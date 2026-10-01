const API = "http://127.0.0.1:8000";


// ============================================================
// DASHBOARD ELEMENTS
// ============================================================

const totalPackets = document.getElementById("totalPackets");
const totalThreats = document.getElementById("totalThreats");
const totalIncidents = document.getElementById("totalIncidents");
const currentAttack = document.getElementById("currentAttack");

const threatProgress = document.getElementById("threatProgress");
const threatLevel = document.getElementById("threatLevel");

const systemDot = document.getElementById("systemDot");
const systemStatus = document.getElementById("systemStatus");

const eventsContainer = document.getElementById("events");


// ============================================================
// CHART DATA
// ============================================================

const trafficLabels = [];
const trafficData = [];

const threatLabels = [
    "DDOS",
    "PORT_SCAN",
    "BOTNET",
    "NORMAL"
];

const threatData = [
    0,
    0,
    0,
    0
];


// ============================================================
// TRAFFIC CHART
// ============================================================

const trafficChart = new Chart(
    document.getElementById("trafficChart"),
    {
        type: "line",

        data: {
            labels: trafficLabels,

            datasets: [
                {
                    label: "Packets",

                    data: trafficData,

                    borderWidth: 2,

                    tension: 0.3,

                    fill: false
                }
            ]
        },

        options: {
            responsive: true,

            animation: false,

            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    }
);


// ============================================================
// THREAT DISTRIBUTION CHART
// ============================================================

const threatChart = new Chart(
    document.getElementById("threatChart"),
    {
        type: "doughnut",

        data: {
            labels: threatLabels,

            datasets: [
                {
                    data: threatData,

                    borderWidth: 1
                }
            ]
        },

        options: {
            responsive: true,

            animation: false
        }
    }
);


// ============================================================
// FETCH SIMULATOR STATUS
// ============================================================

async function updateDashboard() {

    try {

        const response = await fetch(
            `${API}/simulator/status`
        );

        if (!response.ok) {

            throw new Error(
                `HTTP ${response.status}`
            );
        }

        const data = await response.json();

        updateStatistics(data);

        updateThreatLevel(data);

        updateTrafficChart(data);

        updateThreatChart(data);

        updateLiveEvent(data);

    } catch (error) {

        console.error(
            "Dashboard API error:",
            error
        );

        systemStatus.textContent =
            "SYSTEM OFFLINE";

        systemDot.style.background =
            "red";
    }
}


// ============================================================
// UPDATE STATISTICS
// ============================================================

function updateStatistics(data) {

    totalPackets.textContent =
        formatNumber(data.total_packets);

    totalThreats.textContent =
        formatNumber(data.total_threats);

    totalIncidents.textContent =
        formatNumber(data.total_incidents);

    currentAttack.textContent =
        data.current_attack || "NONE";


    // Simulator status

    if (data.running) {

        systemStatus.textContent =
            "SYSTEM ONLINE";

        systemDot.style.background =
            "green";

    } else {

        systemStatus.textContent =
            "SIMULATOR STOPPED";

        systemDot.style.background =
            "orange";
    }
}


// ============================================================
// UPDATE THREAT LEVEL
// ============================================================

function updateThreatLevel(data) {

    const score =
        Number(data.threat_score || 0);


    // Keep score between 0 and 100

    const safeScore =
        Math.max(
            0,
            Math.min(
                100,
                score
            )
        );


    threatProgress.style.width =
        `${safeScore}%`;


    if (safeScore >= 90) {

        threatLevel.textContent =
            "CRITICAL";

    } else if (safeScore >= 70) {

        threatLevel.textContent =
            "HIGH";

    } else if (safeScore >= 40) {

        threatLevel.textContent =
            "MEDIUM";

    } else {

        threatLevel.textContent =
            "LOW";
    }
}


// ============================================================
// UPDATE TRAFFIC CHART
// ============================================================

function updateTrafficChart(data) {

    if (!data.last_event) {
        return;
    }


    const event =
        data.last_event;


    const time =
        new Date(
            event.timestamp
        ).toLocaleTimeString();


    trafficLabels.push(time);

    trafficData.push(
        event.packet_count
    );


    // Keep only latest 20 points

    if (trafficLabels.length > 20) {

        trafficLabels.shift();

        trafficData.shift();
    }


    trafficChart.update();
}


// ============================================================
// UPDATE THREAT DISTRIBUTION
// ============================================================

function updateThreatChart(data) {

    if (!data.last_event) {
        return;
    }


    const attack =
        data.last_event.attack_type;


    if (attack === "DDOS") {

        threatData[0]++;

    } else if (
        attack === "PORT_SCAN"
    ) {

        threatData[1]++;

    } else if (
        attack === "BOTNET"
    ) {

        threatData[2]++;

    } else {

        threatData[3]++;
    }


    threatChart.update();
}


// ============================================================
// LIVE SECURITY EVENT
// ============================================================

function updateLiveEvent(data) {

    if (!data.last_analysis) {
        return;
    }


    const analysis =
        data.last_analysis;

    const traffic =
        data.last_event;


    const event =
        document.createElement("div");

    event.className =
        "event";


    const prediction =
        analysis.prediction ||
        "UNKNOWN";


    const score =
        analysis.threat_score ||
        0;


    const action =
        analysis.response?.action ||
        "NONE";


    const incident =
        analysis.incident_id ||
        "-";


    event.innerHTML = `

        <strong>
            ${prediction}
        </strong>

        &nbsp; | &nbsp;

        Threat Score:
        ${score}

        &nbsp; | &nbsp;

        Defense:
        ${action}

        &nbsp; | &nbsp;

        Incident:
        ${incident}

        <br>

        Source:
        ${traffic?.src_ip || "-"}

        →

        Destination:
        ${traffic?.dst_ip || "-"}

        &nbsp; | &nbsp;

        Protocol:
        ${traffic?.protocol || "-"}

    `;


    eventsContainer.prepend(
        event
    );


    // Keep only latest 10 events

    while (
        eventsContainer.children.length > 10
    ) {

        eventsContainer.removeChild(
            eventsContainer.lastChild
        );
    }
}


// ============================================================
// FORMAT NUMBERS
// ============================================================

function formatNumber(value) {

    if (
        value === undefined ||
        value === null
    ) {

        return "0";
    }


    return Number(value)
        .toLocaleString();
}


// ============================================================
// START DASHBOARD UPDATES
// ============================================================

updateDashboard();


// Update every 2 seconds

setInterval(
    updateDashboard,
    2000
);
// ============================================================
// SIMULATOR CONTROL FUNCTIONS
// ============================================================


async function startSimulator() {

    try {

        const response = await fetch(
            `${API}/simulator/start`,
            {
                method: "POST"
            }
        );

        const data =
            await response.json();

        console.log(
            "Simulator started:",
            data
        );

        updateDashboard();

    } catch (error) {

        console.error(
            "Start simulator error:",
            error
        );

        alert(
            "Unable to start simulator"
        );
    }
}


async function stopSimulator() {

    try {

        const response = await fetch(
            `${API}/simulator/stop`,
            {
                method: "POST"
            }
        );

        const data =
            await response.json();

        console.log(
            "Simulator stopped:",
            data
        );

        updateDashboard();

    } catch (error) {

        console.error(
            "Stop simulator error:",
            error
        );

        alert(
            "Unable to stop simulator"
        );
    }
}


async function changeAttack(
    attackType
) {

    try {

        const response = await fetch(
            `${API}/simulator/attack/${attackType}`,
            {
                method: "POST"
            }
        );

        const data =
            await response.json();

        console.log(
            "Attack changed:",
            data
        );


        if (data.success) {

            document.getElementById(
                "controlAttackStatus"
            ).textContent =
                attackType;

        }


        updateDashboard();

    } catch (error) {

        console.error(
            "Attack change error:",
            error
        );

        alert(
            "Unable to change attack type"
        );
    }
}


// ============================================================
// BUTTON EVENTS
// ============================================================


document.getElementById(
    "startSimulator"
).addEventListener(
    "click",
    startSimulator
);


document.getElementById(
    "stopSimulator"
).addEventListener(
    "click",
    stopSimulator
);


document.getElementById(
    "normalAttack"
).addEventListener(
    "click",
    function () {

        changeAttack("NONE");

    }
);


document.getElementById(
    "ddosAttack"
).addEventListener(
    "click",
    function () {

        changeAttack("DDOS");

    }
);


document.getElementById(
    "portScanAttack"
).addEventListener(
    "click",
    function () {

        changeAttack("PORT_SCAN");

    }
);


document.getElementById(
    "botnetAttack"
).addEventListener(
    "click",
    function () {

        changeAttack("BOTNET");

    }
);
// ============================================================
// 6G SIMULATOR CONTROL PANEL
// ============================================================


async function startSimulator() {

    try {

        const response = await fetch(
            `${API}/simulator/start`,
            {
                method: "POST"
            }
        );

        const data =
            await response.json();

        console.log(
            "START:",
            data
        );

        updateDashboard();

    } catch (error) {

        console.error(
            "Start simulator error:",
            error
        );

        alert(
            "Could not start simulator."
        );
    }
}


// ============================================================
// STOP SIMULATOR
// ============================================================

async function stopSimulator() {

    try {

        const response = await fetch(
            `${API}/simulator/stop`,
            {
                method: "POST"
            }
        );

        const data =
            await response.json();

        console.log(
            "STOP:",
            data
        );

        updateDashboard();

    } catch (error) {

        console.error(
            "Stop simulator error:",
            error
        );

        alert(
            "Could not stop simulator."
        );
    }
}


// ============================================================
// CHANGE ATTACK
// ============================================================

async function changeAttack(
    attackType
) {

    try {

        const response = await fetch(
            `${API}/simulator/attack/${attackType}`,
            {
                method: "POST"
            }
        );

        const data =
            await response.json();

        console.log(
            "ATTACK:",
            data
        );


        if (data.success) {

            document.getElementById(
                "controlAttackStatus"
            ).textContent =
                attackType === "NONE"
                    ? "NORMAL"
                    : attackType;
        }


        updateDashboard();

    } catch (error) {

        console.error(
            "Attack change error:",
            error
        );

        alert(
            "Could not change attack."
        );
    }
}


// ============================================================
// BUTTON EVENTS
// ============================================================

document.getElementById(
    "startSimulator"
).addEventListener(
    "click",
    startSimulator
);


document.getElementById(
    "stopSimulator"
).addEventListener(
    "click",
    stopSimulator
);


document.getElementById(
    "normalAttack"
).addEventListener(
    "click",
    function () {

        changeAttack("NONE");

    }
);


document.getElementById(
    "ddosAttack"
).addEventListener(
    "click",
    function () {

        changeAttack("DDOS");

    }
);


document.getElementById(
    "portScanAttack"
).addEventListener(
    "click",
    function () {

        changeAttack("PORT_SCAN");

    }
);


document.getElementById(
    "botnetAttack"
).addEventListener(
    "click",
    function () {

        changeAttack("BOTNET");

    }
);