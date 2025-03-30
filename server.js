const express = require("express");
const { spawn } = require("child_process");

const app = express();
app.use(express.json());

app.post("/summarize", (req, res) => {
    const text = req.body.text;
    if (!text) {
        return res.status(400).json({ error: "Missing 'text' parameter" });
    }

    // Call Python script
    const pythonProcess = spawn("python", ["classifier.py", text]);

    let result = "";
    pythonProcess.stdout.on("data", (data) => {
        result += data.toString();
    });

    pythonProcess.stderr.on("data", (data) => {
        console.error(`Error: ${data}`);
    });

    pythonProcess.on("close", (code) => {
        if (code === 0) {
            res.json({ summary: result.trim() });
        } else {
            res.status(500).json({ error: "Python script execution failed" });
        }
    });
});

// Start server
const PORT = process.env.PORT || 4000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
