const express = require('express');
const path = require('path');
const { exec } = require('child_process');
const fs = require('fs');
const zip = require('express-zip');
const os = require('os');
const { PythonShell } = require('python-shell'); // Correct import for PythonShell
const cors = require('cors');
const archiver = require('archiver');
const app = express();
app.use(cors());


// app.get('/', (req, res) => {
//     res.sendFile(path.join(__dirname, '/views/index.html'));
// });


// Serve static files from the frontend build directory
app.use(express.static(path.join(__dirname, 'dist/final-project/browser')));

// Serve the main index.html file on the root path
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'dist/final-project/browser/index.html'));
});


//--------Single Game


// Retrieving game list for task
app.get('/single_game/games_list', (req, res) => { 
    const jsonFileName = req.query.task || 'Diamonds.json' 

    if (!jsonFileName) {
        return res.status(400).send('JSON file name is required');
    }

    const jsonFilePath = path.join(__dirname, jsonFileName);
    if (!fs.existsSync(jsonFilePath)) {
        return res.status(404).send('JSON file not found');
    }

    fs.readFile(jsonFilePath, 'utf8', (err, data) => {
        if (err) {
            console.error(`Error reading file: ${err.message}`);
            return res.status(500).send('Error reading file');
        }

        try {
            const jsonData = JSON.parse(data);
            const videoPaths = jsonData.relpaths || [];
            res.json(videoPaths);
        } catch (parseError) {
            console.error(`Error parsing JSON: ${parseError.message}`);
            res.status(500).send('Error parsing JSON');
        }
    });
});


// Retrieving filter lists for game 
app.get('/single_game/inventory_actions' , async (req, res)=> {
    const task= req.query.task || 'diamonds';
    const gameName= req.query.name || 'game1';

    if (!gameName || !task) {
        return res.status(400).send('Game name and Task are required');
    }

    const gamename = 'cheeky-cornflower-setter-0b1e4d5c2f70-20220413-211200.jsonl'; //puting a default game name that exists in our data, remove this when we run on 100%
    const command= `python data_analysis_scripts/Get_Filters_Single.py --task ${task} --gamename ${gamename}`

    try {
        await executeCommand(command, 0);

        fs.readFile('filters_single.json', 'utf8', (err, data) => {
            if (err) {
                console.error('Error reading the file:', err);
                return;
            }
        
            const jsonData = JSON.parse(data);

            // Prepare the response object
            const resFilters = {
                inventory: jsonData.inventory,
                actions: jsonData.actions
            };

            res.json(resFilters);
        });

    } catch (error) {
        res.status(500).send(`Error: ${error.message}`);
    }

});


// Retrieving results after user chooses to analyze
app.get('/single_game/timelines', async (req, res) =>{
    const task= req.query.task || 'diamonds';
    const percentage = req.query.size || 10;
    const res_inventory = JSON.parse(req.query.inventory) || 'white_tulip,stick,dark_oak_planks,gold_ore,dirt';
    const res_actions = JSON.parse(req.query.aggregated_actions) || 'mines.stone,mines.cobblestone,pick-ups.cobblestone,uses.stone';

    //add params checks 

    //const inventory = 'white_tulip,stick,dark_oak_planks,gold_ore,dirt';
    const inventory = res_inventory.map(item => item.name);
    const actions = res_actions.flatMap(item =>
        item.actions.map(action => `${action.replace(/-/g, '_')}.${item.name.replace(/ /g, '_')}`)
    );

    console.log(actions)
    

    const commands = [
        `python data_analysis_scripts/TimeSeriesInventory.py --percentage ${percentage} --inventory ${inventory}`,  
        `python data_analysis_scripts/TimeSeriesStates.py --percentage ${percentage} --actions ${actions}`
    ];

    try {
        // Execute all commands concurrently and wait for all promises to resolve
        const results = await Promise.all(commands.map(command => executeCommand(command)));

        const [inv_timeline, actions_timeline] = await Promise.all([
            fs.promises.readFile(results[0].inv_path),
            fs.promises.readFile(results[1].actions_path),
        ]);

        const response = {
            images: [actions_timeline, inv_timeline],
            data_points: [results[0].inv_points, results[1].actions_points]
        };

        res.json(response)

    } catch (error) {
        res.status(500).send(`Error: ${error.message}`);
    }
});




// ------------Dataset


// Retrieving filter lists for game 
app.get('/dataset/keys_inventory_actions' , async (req, res)=> {
    const task= req.query.task || 'Diamonds';
    const size= req.query.size || 10;

    if (!task || !size) {
        return res.status(400).send('Task and Size are required');
    }

    const command= `python data_analysis_scripts/Get_Filters.py --task ${task} --percentage ${size}`

    try {
        await executeCommand(command, 0);

        fs.readFile('filters_dataset.json', 'utf8', (err, data) => {
            if (err) {
                console.error('Error reading the file:', err);
                return;
            }
        
            const jsonData = JSON.parse(data);

            const keys = jsonData.keys.map(key => key.replace(/^keyboard\./, ''));
            
            // Prepare the response object
            const resFilters = {
                inventory: jsonData.inventory,
                actions: jsonData.actions,
                keys: keys
            };

            res.json(resFilters);
        });

    } catch (error) {
        res.status(500).send(`Error: ${error.message}`);
    }

});


app.get('/dataset/hist', async (req, res) => {
    const task= req.query.task || 'Diamonds';
    const percentage = req.query.size || 100;
    const keys = req.query.keys || 'a,b,c';
    const inventory = JSON.stringify(req.query.inventory) || 'white_tulip,stick,dark_oak_planks,gold_ore,dirt';
    const actions = JSON.stringify(req.query.aggregated_actions) || 'mines.stone,mines.cobblestone,pick-ups.cobblestone,uses.stone';

    //add params checks 

    const command= `python data_analysis_scripts/Histograms.py --percentage ${percentage} --task ${task} --keys ${keys} --inventory ${inventory} --actions ${actions}`

    try {
        await executeCommand(command, 0);

        const archive = archiver('zip', {
            zlib: { level: 9 } 
        });

        // Pipe the archive data to the response
        archive.pipe(res);

        // Add files to the archive
        archive.directory('Histo_Results', 'Histo_Results'); 

        // stream the zip file to the response
        await archive.finalize();

    } catch (error) {
        res.status(500).send(`Error: ${error.message}`);
    }
});


async function actionGraph(task, actions, percentage){

    const command= `python data_analysis_scripts/Actions_Graph_2.0.py --percentage ${percentage} --task ${task} --actions ${actions}`

    try {
        const result = await executeCommand(command);
        // Assuming the result contains the path to the JPEG file
        const jpegPath = result.trim();
        const fullPath = path.resolve(jpegPath);

        console.log('JPEG Path:', fullPath);

        // Read the JPEG file
        const jpegData = await fs.readFile(fullPath);

        return jpegData;
    } catch (error) {
        throw new Error(`Error generating action graph: ${error}`);
    }

}




// 
app.get('/dataset/timelines_stats', async (req, res) =>{
    const percentage = req.query.size || 10;
    const keys = req.query.keys || 'a,b,c';
    const inventory = req.query.inventory || 'white_tulip,stick,dark_oak_planks,gold_ore,dirt';
    const res_actions = JSON.parse(req.query.aggregated_actions) || 'mines.stone,mines.cobblestone,pick-ups.cobblestone,uses.stone';

    //add params checks 

    const actions = res_actions.flatMap(item =>
        item.actions.map(action => `${action.replace(/-/g, '_')}.${item.name.replace(/ /g, '_')}`)
    );

    const commands = [
        `python data_analysis_scripts/TimeSeriesInventory.py --percentage ${percentage} --inventory ${inventory}`,
        `python data_analysis_scripts/TimeSeriesStates.py --percentage ${percentage} --actions ${actions}`,
        `python data_analysis_scripts/Stats.py --percentage ${percentage} --keys ${keys} --inventory ${inventory} --actions ${actions}`,
    ];

    
    try {
        // Execute all commands concurrently and wait for all promises to resolve
        const results = await Promise.all(commands.map(command => executeCommand(command)));

        const [inv_timeline, actions_timeline] = await Promise.all([
            fs.promises.readFile(results[0].inv_path),
            fs.promises.readFile(results[1].actions_path),
        ]);

        const task= 'House_Building.json';
        myactions =JSON.stringify(req.query.aggregated_actions);
        const action_graph = await actionGraph(task, myactions , percentage);

        const response = {
            images: [actions_timeline, inv_timeline, action_graph],
            data_points: [results[0].inv_points, results[1].actions_points],
            stats: results[2].stats
        };

        res.json(response)

    } catch (error) {
        res.status(500).send(`Error: ${error.message}`);
    }
});


// Function to execute a command
function executeCommand(command, idx = -1) {
    return new Promise((resolve, reject) => {
        exec(command, (error, stdout, stderr) => {
            if (error) {
                console.error(`Error executing script: ${error.message}`);
                console.error(`stderr: ${stderr}`);
                reject(error);
            } else {
                console.log(`stdout: ${stdout}`);
                try {
                    var output = ''
                    if (idx == 0){
                        // const zipFilePath = 'histograms.zip';
                        // const zipFileContents = fs.readFileSync(zipFilePath);
                        // output = zipFileContents;
                        
                    }
                    else{
                        output = JSON.parse(stdout);
                    }
                    
                    resolve(output);
                } catch (parseError) {
                    console.error(`Error parsing JSON output: ${parseError.message}`);
                    reject(parseError);
                }
            }
        });
    });
}


// ---------Extra


app.get('/download', (req, res) => {
    const videoPath = req.query.videoPath;
    if (!videoPath) {
        return res.status(400).send('Video path is required');
    }

    // Use temporary directory for downloads
    const outputDir = path.join(os.tmpdir(), 'downloads');
    if (!fs.existsSync(outputDir)) {
        fs.mkdirSync(outputDir);
    }

    // Run the Python script
    const command = `python GetVideo.py --video-path "${videoPath}" --output-dir "${outputDir}"`;
    exec(command, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error executing script: ${error.message}`);
            console.error(`stderr: ${stderr}`);
            return res.status(500).send(`Error executing script: ${error.message}`);
        }
        console.log(`stdout: ${stdout}`);

        const videoFilename = path.basename(videoPath);
        const jsonlFilename = videoFilename.replace('.mp4', '.jsonl');
        const videoOutpath = path.join(outputDir, videoFilename);
        const jsonlOutpath = path.join(outputDir, jsonlFilename);

        // Check if the files were downloaded successfully
        if (fs.existsSync(videoOutpath) && fs.existsSync(jsonlOutpath)) {
            res.zip([
                { path: videoOutpath, name: videoFilename },
                { path: jsonlOutpath, name: jsonlFilename }
            ]);
        } else {
            res.status(500).send('Error downloading files');
        }
    });
});



app.get('/TimeSeriesInvetory', (req, res) => {
    const percentage = req.query.percentage || 100;
    const items = req.query.items || 'white_tulip,stick,dark_oak_planks,gold_ore,dirt';

    console.log(`Received request for analysis with percentage: ${percentage} and items: ${items}`);

    const command = `python data_analysis_scripts/TimeSeriesInventory.py --percentage ${percentage} --items ${items}`;
    exec(command, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error executing script: ${error.message}`);
            console.error(`stderr: ${stderr}`);
            return res.status(500).send(`Error executing script: ${error.message}`);
        }
        console.log(`stdout: ${stdout}`);
        try {
            const output = JSON.parse(stdout);
            res.json(output);
        } catch (parseError) {
            console.error(`Error parsing JSON output: ${parseError.message}`);
            res.status(500).send(`Error parsing JSON output: ${parseError.message}`);
        }
    });
});

app.get('/TimeSeriesStates', (req, res) => {
    const percentage = req.query.percentage || 100;
    const items = req.query.items || 'mines.stone,mines.cobblestone,pick-ups.cobblestone,uses.stone pickaxe';

    console.log(`Received request for analysis with percentage: ${percentage} and items: ${items}`);

    const command = `python data_analysis_scripts/TimeSeriesStates.py --percentage ${percentage} --items "${items}"`;
    exec(command, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error executing script: ${error.message}`);
            console.error(`stderr: ${stderr}`);
            return res.status(500).send(`Error executing script: ${error.message}`);
        }
        console.log(`stdout: ${stdout}`);
        try {
            const output = JSON.parse(stdout);
            res.json(output);
        } catch (parseError) {
            console.error(`Error parsing JSON output: ${parseError.message}`);
            res.status(500).send(`Error parsing JSON output: ${parseError.message}`);
        }
    });
});

const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
    console.log(`App deployed at Port ${PORT}`);
});


