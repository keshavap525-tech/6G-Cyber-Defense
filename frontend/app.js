const API = "http://127.0.0.1:8000";

async function getSimulatorStatus() {
    try {
        const response = await fetch(`${API}/simulator/status`);

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        const data = await response.json();

        updateDashboard(data);

    } catch (error) {

        console.error("Simulator API error:", error);

        setText("system-status", "OFFLINE");
    }
}


function updateDashboard(data) {

    // Simulator status
    setText(
        "system-status",
        data.running ? "RUNNING" : "STOPPED"
    );

    // Statistics
    setText(
        "total-packets",
        formatNumber(data.total_packets)
    );

    setText(
        "total-threats",
        formatNumber(data.total_threats)
    );

    setText(
        "total-incidents",
        formatNumber(data.total_incidents)
    );

    // Current attack
    setText(
        "current-attack",
        data.current_attack || "NONE"
    );

    // Threat score
    setText(
        "threat-score",
        data.threat_score ?? 0
    );

    // Latest detection
    if (data.last_analysis) {

        setText(
            "prediction",
            data.last_analysis.prediction || "UNKNOWN"
        );

        setText(
            "confidence",
            `${Math.round(
                (data.last_analysis.confidence || 0) * 100
            )}%`
        );

        setText(
            "defense-action",
            data.last_analysis.response?.action || "NONE"
        );

        setText(
            "severity",
            data.last_analysis.threat_analysis?.severity || "LOW"
        );

        setText(
            "incident-id",
            data.last_analysis.incident_id || "-"
        );
    }

    // Latest traffic
    if (data.last_event) {

        setText(
            "source-ip",
            data.last_event.src_ip || "-"
        );

        setText(
            "destination-ip",
            data.last_event.dst_ip || "-"
        );

        setText(
            "protocol",
            data.last_event.protocol || "-"
        );

        setText(
            "packet-count",
            formatNumber(data.last_event.packet_count)
        );
    }
}


function setText(id, value) {

    const element = document.getElementById(id);

    if (element) {
        element.textContent = value;
    }
}


function formatNumber(value) {

    if (value === undefined || value === null) {
        return "0";
    }

    return Number(value).toLocaleString();
}


// Refresh dashboard every 2 seconds
setInterval(
    getSimulatorStatus,
    2000
);


// Load immediately
getSimulatorStatus();