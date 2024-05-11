import express from 'express';
import bodyParser from 'body-parser';
import cors from 'cors'; 
import fs from 'fs';

const app = express();
const PORT = 5000;

app.use(bodyParser.json());
app.use(cors());

app.get('/api', async (req, res) => {

    const size = parseInt(req.query["size"]);

    // Perform a simple check on the parameters
    if (!size) {
        return res.status(400).send('Missing parameters');
    }

    const gameStatsPath = `C:\\Users\\ASUS\\Desktop\\assets\\Games_Statistics.json`; 
    const distPath = `C:\\Users\\ASUS\\Desktop\\assets\\dist\\distribution_game_durations${size}.png`;
    const timeline1Path = `C:\\Users\\ASUS\\Desktop\\assets\\action_freq\\action_frequencies_${size}pct.png`;
    const timeline2Path = `C:\\Users\\ASUS\\Desktop\\assets\\inventory_freq\\inventory_frequencies_${size}pct.png`;

    try {
        // Read JSON file
        const gameStatsData = await fs.promises.readFile(gameStatsPath, 'utf8');
        const gameStats = JSON.parse(gameStatsData);

        // Read images
        const [distData, timeline1Data, timeline2Data] = await Promise.all([
            fs.promises.readFile(distPath),
            fs.promises.readFile(timeline1Path),
            fs.promises.readFile(timeline2Path)
        ]);

        const stats = {};

        for (const key in gameStats[size.toString()]) {
            const [avg, [min, max], stdDev] = gameStats[size.toString()][key];
        
            stats[key] = {
                avg: avg,
                min: min, 
                max: max,
                stdDeviation: stdDev
            };
        }

        // Construct the response object
        const response = {
            images: [distData, timeline1Data, timeline2Data, null, null, null, null],
            stats: stats
        };

        // Send the response
        res.json(response);
    } catch (err) {
        console.error('Error:', err);
        res.status(500).send('Internal Server Error');
    }

});




app.listen(PORT, ()=> console.log(`Server running on port ${PORT}`));