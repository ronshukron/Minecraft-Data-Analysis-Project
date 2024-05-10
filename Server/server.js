const express = require('express');
const path = require('path');
const { exec } = require('child_process');
const fs = require('fs');
const zip = require('express-zip');
const os = require('os');

const app = express();

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, '/views/index.html'));
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


app.get('/check-python', (req, res) => {
    exec('python --version', (error, stdout, stderr) => {
        if (error) {
            console.error(`Error checking Python: ${error.message}`);
            console.error(`stderr: ${stderr}`);
            return res.status(500).send(`Error checking Python: ${error.message}`);
        }
        res.send(`Python version: ${stdout}`);
    });
});


const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
    console.log(`App deployed at Port ${PORT}`);
});
