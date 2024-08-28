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
// Helper function to transform game name
function transformGameName(filePath) {
    const match = filePath.match(/\d{8}-\d{6}/);
    if (match) {
        return `merged_run_${match[0]}.json`;
    } else {
        throw new Error("Invalid file name format.");
    }
}
// Retrieving game list for task
app.get('/single_game/games_list', (req, res) => { 
    const jsonFileName = req.query.task || 'Diamonds.json';

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
            
            const actual_task = jsonFileName.split('.')[0];
            // Get list of files in Parsed_Data/100 directory
            const parsedDataDir_old = path.join(__dirname, 'Parsed_Data', '100');
            const parsedDataDir = `C:/Data/${actual_task}/100`;
            fs.readdir(parsedDataDir, (err, files) => {
                if (err) {
                    console.error(`Error reading directory: ${err.message}`);
                    return res.status(500).send('Error reading directory');
                }

                // Transform the video paths to the expected format and filter out the non-existent ones
                const existingFiles = files.filter(file => file.endsWith('.json'));
                const existingGameNames = videoPaths.filter(videoPath => {
                    try {
                        const transformedName = transformGameName(videoPath);
                        return existingFiles.includes(transformedName);
                    } catch (e) {
                        return false;
                    }
                });

                res.json(existingGameNames);
            });
        } catch (parseError) {
            console.error(`Error parsing JSON: ${parseError.message}`);
            res.status(500).send('Error parsing JSON');
        }
    });
});

// // Retrieving game list for task
// app.get('/single_game/games_list', (req, res) => { 
//     const jsonFileName = req.query.task || 'Diamonds.json' 

//     if (!jsonFileName) {
//         return res.status(400).send('JSON file name is required');
//     }

//     const jsonFilePath = path.join(__dirname, jsonFileName);
//     if (!fs.existsSync(jsonFilePath)) {
//         return res.status(404).send('JSON file not found');
//     }

//     fs.readFile(jsonFilePath, 'utf8', (err, data) => {
//         if (err) {
//             console.error(`Error reading file: ${err.message}`);
//             return res.status(500).send('Error reading file');
//         }

//         try {
//             const jsonData = JSON.parse(data);
//             const videoPaths = jsonData.relpaths || [];
//             res.json(videoPaths);
//         } catch (parseError) {
//             console.error(`Error parsing JSON: ${parseError.message}`);
//             res.status(500).send('Error parsing JSON');
//         }
//     });
// });


// Retrieving filter lists for game 
app.get('/single_game/inventory_actions' , async (req, res)=> {
    const task= req.query.task || 'diamonds';
    const gameName= req.query.name || 'game1';

    if (!gameName || !task) {
        return res.status(400).send('Game name and Task are required');
    }

    const gamename = 'cheeky-cornflower-setter-0b1e4d5c2f70-20220413-211200.jsonl'; //puting a default game name that exists in our data, remove this when we run on 100%
    const command= `python data_analysis_scripts/Get_Filters_Single.py --task ${task} --gamename ${gameName}`

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
    const percentage = req.query.size || 0;
    const game_name = req.query.name || null;  // ron added
    const res_inventory = JSON.parse(req.query.inventory) || 'white_tulip,stick,dark_oak_planks,gold_ore,dirt';
    const res_actions = JSON.parse(req.query.aggregated_actions) || 'mines.stone,mines.cobblestone,pick-ups.cobblestone,uses.stone';

    //add params checks 

    //const inventory = 'white_tulip,stick,dark_oak_planks,gold_ore,dirt';
    const inventory = res_inventory.map(item => item.name);
    const actions = res_actions.flatMap(item =>
        item.actions.map(action => `${action.replace(/-/g, '_')}.${item.name.replace(/ /g, '_')}`)
    );
    console.log(res_inventory)

    console.log(inventory)
    

    const commands = [
        `python data_analysis_scripts/SingleTimeSeriesStates.py --actions ${actions.join(',')} --game_name ${game_name} --task ${task}`,
        `python data_analysis_scripts/SingleTimeSeriesInventory.py --inventory "${res_inventory.join(',')}" --game_name "${game_name}" --task ${task}`
    ];
    
    try {
        // Execute all commands concurrently and wait for all promises to resolve
        const results = await Promise.all(commands.map(command => executeCommand(command)));

        // const [inv_timeline, actions_timeline] = await Promise.all([
        //     // fs.promises.readFile(results[0].inv_path),
        //     fs.promises.readFile(results.actions_path),
        // ]);
        console.log(results[0].actions_path)
        console.log(results[1].inv_path)

        const [inv_timeline, actions_timeline] = await Promise.all([
            fs.promises.readFile(results[1].inv_path),
            fs.promises.readFile(results[0].actions_path),
        ]);


        const response = {
            images: [inv_timeline, actions_timeline],
            // images: [actions_timeline, inv_timeline],
            // data_points: [inventory_data.inv_points, results.actions_points]
            // data_points: [results[1].actions_points]
            data_points: [results[1].inv_points, results[0].actions_points]
        };

        res.json(response)

    } catch (error) {
        res.status(500).send(`Error: ${error.message}`);
    }
});



// app.get('/single_game/timelines', async (req, res) => {
//     const task = req.query.task || 'diamonds';
//     const percentage = req.query.size || 0;
//     const game_name = req.query.name || null;  // Added to handle specific game file
//     const res_inventory = JSON.parse(req.query.inventory) || ['white_tulip', 'stick', 'dark_oak_planks', 'gold_ore', 'dirt'];
//     const res_actions = JSON.parse(req.query.aggregated_actions) || [{ name: 'stone', actions: ['mines', 'uses'] }];

//     // Convert inventory and actions to the format needed for the script
//     const inventory = res_inventory.map(item => item.name);
//     const actions = res_actions.flatMap(item => 
//         item.actions.map(action => `${action.replace(/-/g, '_')}.${item.name.replace(/ /g, '_')}`)
//     );

//     // Form the command to execute the Python script
//     const command = `python data_analysis_scripts/SingleTimeSeriesStates.py --actions "${actions.join(',')}" --game_name "${game_name}"`;

//     try {
//         // Execute the command and get the result
//         const result = await executeCommand(command);
//         const parsedResult = JSON.parse(result);

//         // Read the image file and convert it to base64
//         const imageBuffer = await fs.promises.readFile(parsedResult.actions_path);
//         const imageBase64 = imageBuffer.toString('base64');

//         // Prepare the response
//         const response = {
//             images: [imageBase64],
//             data_points: [JSON.parse(parsedResult.actions_points)]
//         };

//         res.json(response);

//     } catch (error) {
//         res.status(500).send(`Error: ${error.message}`);
//     }
// });





// ------------Dataset


// Retrieving filter lists for game 
app.get('/dataset/keys_inventory_actions' , async (req, res)=> {
    const task= req.query.task || 'Diamonds';
    const size= req.query.size || 10;
    const actual_task = task.split('.')[0];

    if (!task || !size) {
        return res.status(400).send('Task and Size are required');
    }

    // const command= `python data_analysis_scripts/Get_Filters.py --task ${task} --percentage ${size}`

    try {
        // await executeCommand(command, 0);
        const filePath = `C:\\Data\\Filters\\${actual_task}\\${size}\\filters_dataset.json`;
        fs.readFile(filePath, 'utf8', (err, data) => {
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

//----------------------------------------------------------------------

async function executeCommand1(command) {
    return new Promise((resolve, reject) => {
        exec(command, (error, stdout, stderr) => {
            if (error) {
                reject(`Error executing command: ${stderr}`);
            } else {
                resolve(stdout);
            }
        });
    });
}

async function actionGraph(task, actions, percentage){

    const command= `python data_analysis_scripts/Actions_Graph_2.0.py --percentage ${percentage} --task ${task} --actions ${actions}`

    try {
        await executeCommand1(command);

        console.log("do we get here?")
        const graphPath = path.join(__dirname, 'actions_graph.jpeg');
        // Read the JPEG file
        const jpegData = await fs.readFile(graphPath);

        return jpegData;
    } catch (error) {
        throw new Error(`Error generating action graph: ${error}`);
    }

}

//----------------------------------------------------------------------



// 
app.get('/dataset/timelines_stats', async (req, res) =>{
    const percentage = req.query.size || 10;
    //this is the original: 
    const actions =  req.query.aggregated_actions; // ron changed from req.query.actions
    // this is what im trying instead:
    //const actions = JSON.stringify(req.query.aggregated_actions) || 'mines.stone,mines.cobblestone,pick-ups.cobblestone,uses.stone';
    const task = req.query.task || 'Diamonds';

    const inventory = req.query.inventory || 'white_tulip,stick,dark_oak_planks,gold_ore,dirt';
    const keys = req.query.keys || 'a,b,c';

    //add params checks 
    // Split the string into an array
    const actionsArray = actions.split(',');
    const inventoryArray = inventory.split(',');
    console.log("actions:")
    console.log(actionsArray)

    // Transform the array items
    const res_actions = actionsArray.map(action => action.replace(/-/g, '_'));
    const res_inventory = inventoryArray.map(item => item.replace(/ /g, "_"));
    // const inv = 
    console.log(res_actions)

    const commands = [
        `python data_analysis_scripts/TimeSeriesInventory.py --percentage ${percentage} --inventory ${res_inventory.join(',')} --task ${task}`,
        `python data_analysis_scripts/TimeSeriesStates.py --percentage ${percentage} --actions ${res_actions.join(',')} --task ${task}`,
        `python data_analysis_scripts/Stats.py --percentage ${percentage} --keys ${keys} --inventory ${res_inventory} --actions ${res_actions}`,
    ];

    
    try {
        // Execute all commands concurrently and wait for all promises to resolve
        const results = await Promise.all(commands.map(command => executeCommand(command)));

        const [inv_timeline, actions_timeline] = await Promise.all([
            fs.promises.readFile(results[0].inv_path),
            fs.promises.readFile(results[1].actions_path),
        ]);

        // console.log("before action log script")

        // const task= 'House_Building.json';

        // const actionsJ = JSON.parse(req.query.aggregated_actions);
        // const actionsJSON = JSON.stringify(req.query.aggregated_actions).replace(/"/g, '\\"');

        // const action_graph = await actionGraph(task, actionsJSON , percentage);

        // console.log("after action log script")

        const response = {
            images: [actions_timeline, inv_timeline],
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


