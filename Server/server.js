const express = require('express');
const path = require('path');
const { exec } = require('child_process');
const fs = require('fs');
const zip = require('express-zip');
const os = require('os');
const { PythonShell } = require('python-shell'); // Correct import for PythonShell
const cors = require('cors');
const app = express();

app.use(cors());


app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, '/views/index.html'));
});



//--------Single Game


// Retrieving game list for task
app.get('/single_game/games_list', (req, res) => { //changed api call 
    const jsonFileName = req.query.task; //changed name of param
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
app.get('/single_game/inventory_actions' , (req, res)=> {
    const gameName= req.query.game;
    const task= req.query.task;
    if (!gameName || !task) {
        return res.status(400).send('Game name and Task are required');
    }

    const inventory = ['furnace', 'rotten_flesh', 'granite', 'white_bed', 'feather', 'dirt', 'light_gray_wool', 'acacia_planks', 'chicken', 'dark_oak_planks', 'bucket',
     'coal', 'sugar_cane', 'bread', 'oak_log', 'gold_ore', 'porkchop', 'white_wool', 'oak_planks', 'poppy', 'cooked_porkchop'];
    const actions = ['furnace', 'lapis_ore', 'tall_grass', 'stone', 'granite', 'coal_ore', 'dirt', 'dead_bush', 'sugar_cane', 'infested_stone', 'diamond_ore', 'oak_log', 
    'birch_leaves', 'grass_block', 'gold_ore', 'poppy', 'torch', 'lilac', 'melon', 'dark_oak_log'];

    const resFilters = {
        inventory: inventory,
        actions: actions
    };

    res.json(resFilters);

});



// Retrieving results after user chooses to analyze
app.get('/single_game/all_data', (req, res) =>{
    const task= req.query.task;
    const gameName= req.query.game;
    const inventory= req.query.inventory;
    const actions= req.query.actions;

    // if (!gameName || !task || !inventory || !actions) {
    //     return res.status(400).send('Params are missing');
    // }

    //console.log(`Received request for analysis with percentage: ${percentage} and items: ${items}`);

    percentage = 30;
    items = ['dirt','grass'];

    const command = `python data_analysis_scripts/Histograms.py --percentage ${percentage} --items ${items}`;
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



// ------------Dataset

// Define your route handler
app.get('/dataset/all_data', async (req, res) => {
    const percentage = req.query.percentage || 100;
    const keys = req.query.keys || 'a,b,c';
    const inventory = req.query.inventory || 'white_tulip,stick,dark_oak_planks,gold_ore,dirt';
    const actions = req.query.actions || 'mines.stone,mines.cobblestone,pick-ups.cobblestone,uses.stone pickaxe';

    //console.log(`Received request for analysis with percentage: ${percentage} and items: ${items}`);

    //add params checks 

    // const commands = [
    //     `python data_analysis_scripts/TimeSeriesInventory.py --percentage ${percentage} --items ${items}`,
    //     `python data_analysis_scripts/TimeSeriesStates.py --percentage ${percentage} --items "${items}"`,
    //     `python data_analysis_scripts/Histograms.py --percentage ${percentage} --items ${items}`
    // ];

    const commands = [
        // `python data_analysis_scripts/TimeSeriesInventory.py --percentage ${percentage} --items ${inventory}`,
        // `python data_analysis_scripts/TimeSeriesStates.py --percentage ${percentage} --items "${actions}"`,
           `python data_analysis_scripts/Stats.py --percentage ${percentage} --keys ${keys} --inventory ${inventory} --actions ${actions}`

    ];

    try {
        // Execute all commands concurrently and wait for all promises to resolve
        const results = await Promise.all(commands.map(command => executeCommand(command)));

        // Send the results
        res.json(results);
    } catch (error) {
        // Handle any errors
        res.status(500).send(`Error: ${error.message}`);
    }
});


// Retrieving filter lists for game 
app.get('/dataset/keys_inventory_actions' , (req, res)=> {
    const task= req.query.task;
    const size= req.query.size;
    if (!task || !size) {
        return res.status(400).send('Task and Size are required');
    }

    const keys = ['key.keyboard.e', 'key.keyboard.q', 'key.keyboard.n', 'key.keyboard.b', 'key.keyboard.f2', 'key.keyboard.7', 'key.keyboard.r', 'key.keyboard.left.control',
     'key.keyboard.w', 'key.keyboard.2', 'key.keyboard.m', 'key.keyboard.escape', 'key.keyboard.comma', 'key.keyboard.caps.lock', 'key.keyboard.a', 'key.keyboard.3',
      'key.keyboard.f', 'key.keyboard.space', 'key.keyboard.1', 'key.keyboard.grave.accent'];

    const inventory = ['furnace', 'rotten_flesh', 'granite', 'white_bed', 'feather', 'dirt', 'light_gray_wool', 'acacia_planks', 'chicken', 'dark_oak_planks', 'bucket',
     'coal', 'sugar_cane', 'bread', 'oak_log', 'gold_ore', 'porkchop', 'white_wool', 'oak_planks', 'poppy', 'cooked_porkchop'];

    const actions = ['furnace', 'lapis_ore', 'tall_grass', 'stone', 'granite', 'coal_ore', 'dirt', 'dead_bush', 'sugar_cane', 'infested_stone', 'diamond_ore', 'oak_log', 
    'birch_leaves', 'grass_block', 'gold_ore', 'poppy', 'torch', 'lilac', 'melon', 'dark_oak_log'];

    const resFilters = {
        keys: keys,
        inventory: inventory,
        actions: actions
    };

    res.json(resFilters);

});


// Function to execute a command
function executeCommand(command) {
    return new Promise((resolve, reject) => {
        exec(command, (error, stdout, stderr) => {
            if (error) {
                console.error(`Error executing script: ${error.message}`);
                console.error(`stderr: ${stderr}`);
                reject(error);
            } else {
                console.log(`stdout: ${stdout}`);
                try {
                    const output = JSON.parse(stdout);
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
