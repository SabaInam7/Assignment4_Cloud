require("dotenv").config();
const express = require("express");
const mongoose = require("mongoose");

const app = express();
const PORT = 3000;

app.use(express.json());
app.use(express.static("public"));

// MongoDB connection
mongoose.connect(process.env.MONGO_URL)
.then(() => console.log("MongoDB Connected Successfully"))
.catch(err => console.log("MongoDB Error:", err));

// Calculation schema
const calculationSchema = new mongoose.Schema({
    principal: Number,
    rate: Number,
    months: Number,
    emi: Number,
    servedBy: String,
    createdAt: {
        type: Date,
        default: Date.now
    }
});

const Calculation = mongoose.model("Calculation", calculationSchema);

// EMI API
app.post("/api/emi", async (req, res) => {
    try {
        const { P, rate, n } = req.body;

        if (
            typeof P !== "number" || !Number.isFinite(P) || P <= 0 ||
            typeof rate !== "number" || !Number.isFinite(rate) || rate <= 0 ||
            typeof n !== "number" || !Number.isInteger(n) || n <= 0
        ) {
            return res.status(400).json({
                error: "Enter positive valid numbers."
            });
        }

        const r = rate / 12 / 100;

        const emi = P * r * Math.pow(1 + r, n) /
                    (Math.pow(1 + r, n) - 1);

        const totalPayment = emi * n;
        const totalInterest = totalPayment - P;

        const servedBy = process.env.HOSTNAME || "local";

        const saved = await Calculation.create({
            principal: P,
            rate,
            months: n,
            emi,
            servedBy
        });

        res.json({
            emi: Number(emi.toFixed(2)),
            totalPayment: Number(totalPayment.toFixed(2)),
            totalInterest: Number(totalInterest.toFixed(2)),
            servedBy,
            ipAddress: req.socket.localAddress,
            calculationId: saved._id
        });

    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// History API
app.get("/api/history", async (req, res) => {
    try {
        const history = await Calculation.find()
            .sort({ createdAt: -1 })
            .limit(10);

        res.json(history);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Health API
app.get("/health", async (req, res) => {
    try {
        if (mongoose.connection.readyState !== 1) {
            return res.status(503).send("MongoDB unavailable");
        }

        await mongoose.connection.db.admin().ping();
        res.status(200).send("OK");
    } catch (error) {
        res.status(503).send("MongoDB unavailable");
    }
});

app.listen(PORT, "0.0.0.0", () => {
    console.log(`Server running on port ${PORT}`);
});

