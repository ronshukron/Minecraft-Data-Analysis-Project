const express = require('express');
const path = require('path');
const { exec } = require('child_process');
const fs = require('fs');
const zip = require('express-zip');
const os = require('os');
const { PythonShell } = require('python-shell'); // Correct import for PythonShell

const app = express();

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, '/views/index.html'));
});

app.get('/get-video-paths', (req, res) => {
    const jsonFileName = req.query.jsonFile;
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
