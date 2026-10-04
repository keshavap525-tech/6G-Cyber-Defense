const API = "";

let threatTimelineChart = null;
let attackDistributionChart = null;

let threatHistory = [];
let normalTrafficCount = 0;

const MAX_POINTS = 20;


// =====================================================
// HELPER
// =====================================================

function getElement(id) {
    return document.getElementById(id);
}


// =====================================================
// API
// =====================================================

async function api(url, options = {}) {

    try {

        const response = await fetch(API + url, options);

        if (!response.ok) {
            throw new Error("HTTP " + response.status);
        }

        return await response.json();

    } catch (error) {

        console.error("API ERROR:", error);

        return null;
    }
}


// =====================================================
// SYSTEM STATUS
// =====================================================

async function updateSystemStatus() {

    const data = await api("/simulator/status");

    const status = getElement("systemStatus");

    if (!status) {
        return;
    }

    if (data) {

        status.textContent =
            data.running
                ? "BACKEND ONLINE"
                : "SYSTEM READY";

    } else {

        status.textContent =
            "BACKEND OFFLINE";
    }
}


// =====================================================
// SIMULATOR DATA
// =====================================================

async function updateSimulator() {

    const data =
        await api("/simulator/status");

    if (!data) {
        return;
    }


    // -------------------------------------------------
    // MAIN STATISTICS
    // -------------------------------------------------

    const totalPackets =
        getElement("totalPackets");

    if (totalPackets) {

        totalPackets.textContent =
            Number(
                data.total_packets || 0
            ).toLocaleString();
    }


    const totalThreats =
        getElement("totalThreats");

    if (totalThreats) {

        totalThreats.textContent =
            Number(
                data.total_threats || 0
            ).toLocaleString();
    }


    const totalIncidents =
        getElement("totalIncidents");

    if (totalIncidents) {

        totalIncidents.textContent =
            Number(
                data.total_incidents || 0
            ).toLocaleString();
    }


    const currentAttack =
        getElement("currentAttack");

    if (currentAttack) {

        currentAttack.textContent =
            data.current_attack || "NONE";
    }


    const controlAttackStatus =
        getElement("controlAttackStatus");

    if (controlAttackStatus) {

        controlAttackStatus.textContent =
            data.current_attack || "NONE";
    }


    // -------------------------------------------------
    // LAST EVENT
    // -------------------------------------------------

    const event =
        data.last_event || {};

    const analysis =
        data.last_analysis || {};

    const threatScore =
        Number(
            analysis.threat_score || 0
        );


    // -------------------------------------------------
    // NETWORK METRICS
    // -------------------------------------------------

    const latestPackets =
        getElement("latestPackets");

    if (latestPackets) {

        latestPackets.textContent =
            Number(
                event.packet_count || 0
            ).toLocaleString();
    }


    const latestBytes =
        getElement("latestBytes");

    if (latestBytes) {

        latestBytes.textContent =
            Number(
                event.bytes || 0
            ).toLocaleString();
    }


    const mlConfidence =
        getElement("mlConfidence");

    if (mlConfidence) {

        mlConfidence.textContent =
            Math.round(
                Number(
                    analysis.confidence || 0
                ) * 100
            ) + "%";
    }


    const riskScore =
        getElement("riskScore");

    if (riskScore) {

        riskScore.textContent =
            Math.round(threatScore);
    }


    // -------------------------------------------------
    // DEFENSE PANEL
    // -------------------------------------------------

    const defenseAttack =
        getElement("defenseAttack");

    if (defenseAttack) {

        defenseAttack.textContent =
            analysis.prediction || "NONE";
    }


    const defenseThreatScore =
        getElement("defenseThreatScore");

    if (defenseThreatScore) {

        defenseThreatScore.textContent =
            Math.round(threatScore);
    }


    const threatAnalysis =
        analysis.threat_analysis || {};

    const defenseRecommended =
        getElement("defenseRecommended");

    if (defenseRecommended) {

        defenseRecommended.textContent =
            threatAnalysis.recommended_action ||
            "MONITOR";
    }


    const response =
        analysis.response || {};

    const defenseResponse =
        getElement("defenseResponse");

    if (defenseResponse) {

        defenseResponse.textContent =
            response.action || "NONE";
    }


    const defenseMessage =
        getElement("defenseMessage");

    if (defenseMessage) {

        if (analysis.is_attack) {

            defenseMessage.textContent =
                "Threat detected: " +
                (analysis.prediction || "UNKNOWN") +
                " | Automated defense response active.";

        } else {

            defenseMessage.textContent =
                "System is monitoring simulated 6G network traffic.";
        }
    }


    // -------------------------------------------------
    // THREAT LEVEL
    // -------------------------------------------------

    updateThreatLevel(threatScore);


    // -------------------------------------------------
    // THREAT TIMELINE
    // -------------------------------------------------

    addThreatHistory(threatScore);


    // -------------------------------------------------
    // NORMAL TRAFFIC
    // -------------------------------------------------

    if (
        String(
            event.attack_type || ""
        ).toUpperCase() === "NORMAL"
    ) {

        normalTrafficCount++;
    }


    const normalCount =
        getElement("normalCount");

    if (normalCount) {

        normalCount.textContent =
            normalTrafficCount;
    }
}


// =====================================================
// THREAT LEVEL
// =====================================================

function updateThreatLevel(score) {

    score =
        Math.max(
            0,
            Math.min(
                100,
                Number(score) || 0
            )
        );


    const progress =
        getElement("threatProgress");

    if (progress) {

        progress.style.width =
            score + "%";
    }


    let level = "LOW";


    if (score >= 75) {

        level = "CRITICAL";

    } else if (score >= 50) {

        level = "HIGH";

    } else if (score >= 25) {

        level = "MEDIUM";
    }


    const threatLevel =
        getElement("threatLevel");

    if (threatLevel) {

        threatLevel.textContent =
            level;
    }
}


// =====================================================
// THREAT HISTORY
// =====================================================

function addThreatHistory(score) {

    threatHistory.push({

        time:
            new Date().toLocaleTimeString(),

        score:
            Number(score) || 0
    });


    if (
        threatHistory.length >
        MAX_POINTS
    ) {

        threatHistory.shift();
    }


    updateThreatTimelineChart();
}


// =====================================================
// THREAT SCORE TIMELINE
// =====================================================

function updateThreatTimelineChart() {

    const container =
        document.getElementById("threatTimelineChart");

    if (!container) {
        return;
    }

    if (!threatHistory.length) {
        return;
    }

    const width = 900;
    const height = 280;

    const paddingLeft = 45;
    const paddingRight = 20;
    const paddingTop = 20;
    const paddingBottom = 35;

    const graphWidth =
        width - paddingLeft - paddingRight;

    const graphHeight =
        height - paddingTop - paddingBottom;


    const values = threatHistory.map(
        item => Math.max(
            0,
            Math.min(
                100,
                Number(item.score) || 0
            )
        )
    );


    const points = values.map(
        (value, index) => {

            const x =
                paddingLeft +
                (
                    index /
                    Math.max(
                        values.length - 1,
                        1
                    )
                ) *
                graphWidth;

            const y =
                paddingTop +
                graphHeight -
                (
                    value / 100
                ) *
                graphHeight;

            return {
                x,
                y,
                value
            };
        }
    );


    let linePath = "";

    points.forEach(
        (point, index) => {

            linePath +=
                index === 0
                    ? `M ${point.x} ${point.y}`
                    : ` L ${point.x} ${point.y}`;
        }
    );


    const areaPath =
        linePath +
        ` L ${points[points.length - 1].x} ${
            paddingTop + graphHeight
        }` +
        ` L ${points[0].x} ${
            paddingTop + graphHeight
        } Z`;


    let grid = "";


    for (
        let value = 0;
        value <= 100;
        value += 20
    ) {

        const y =
            paddingTop +
            graphHeight -
            (value / 100) *
            graphHeight;


        grid += `
            <line
                class="timeline-grid"
                x1="${paddingLeft}"
                y1="${y}"
                x2="${width - paddingRight}"
                y2="${y}"
            />

            <text
                x="5"
                y="${y + 5}"
                fill="#8f9bb3"
                font-size="12"
            >
                ${value}
            </text>
        `;
    }


    let circles = "";


    points.forEach(
        point => {

            circles += `
                <circle
                    class="timeline-point"
                    cx="${point.x}"
                    cy="${point.y}"
                    r="4"
                >
                    <title>
                        Threat Score: ${point.value}
                    </title>
                </circle>
            `;
        }
    );


    container.innerHTML = `

        <svg
            viewBox="0 0 ${width} ${height}"
            preserveAspectRatio="none"
        >

            ${grid}

            <path
                class="timeline-area"
                d="${areaPath}"
            />

            <path
                class="timeline-line"
                d="${linePath}"
            />

            ${circles}

            <text
                x="${width / 2}"
                y="${height - 5}"
                text-anchor="middle"
                fill="#8f9bb3"
                font-size="12"
            >
                Real-Time Threat Score
            </text>

        </svg>
    `;
}
// =====================================================
// INCIDENTS
// =====================================================

async function updateIncidents() {

    const data =
        await api("/incidents/");


    if (!data) {
        return;
    }


    const incidents =
        Array.isArray(data)
            ? data
            : (
                data.incidents || []
            );


    updateAttackCounters(
        incidents
    );


    updateIncidentTable(
        incidents
    );


    updateAttackDistribution(
        incidents
    );
}


// =====================================================
// ATTACK COUNTERS
// =====================================================

function updateAttackCounters(
    incidents
) {

    let ddos = 0;
    let portScan = 0;
    let botnet = 0;


    incidents.forEach(
        incident => {

            const type =
                String(
                    incident.attack_type ||
                    incident.prediction ||
                    ""
                ).toUpperCase();


            if (type === "DDOS") {

                ddos++;

            } else if (
                type === "PORT_SCAN" ||
                type === "PORT SCAN"
            ) {

                portScan++;

            } else if (
                type === "BOTNET"
            ) {

                botnet++;
            }
        }
    );


    const ddosCount =
        getElement("ddosCount");

    if (ddosCount) {

        ddosCount.textContent =
            ddos;
    }


    const portScanCount =
        getElement("portScanCount");

    if (portScanCount) {

        portScanCount.textContent =
            portScan;
    }


    const botnetCount =
        getElement("botnetCount");

    if (botnetCount) {

        botnetCount.textContent =
            botnet;
    }
}


// =====================================================
// ATTACK DISTRIBUTION
// =====================================================

function updateAttackDistribution(
    incidents
) {

    const canvas =
        getElement(
            "attackDistributionChart"
        );


    if (!canvas) {
        return;
    }


    if (
        typeof Chart === "undefined"
    ) {
        return;
    }


    let ddos = 0;
    let portScan = 0;
    let botnet = 0;
    let normal = 0;


    incidents.forEach(
        incident => {

            const type =
                String(
                    incident.attack_type ||
                    incident.prediction ||
                    ""
                ).toUpperCase();


            if (type === "DDOS") {

                ddos++;

            } else if (
                type === "PORT_SCAN" ||
                type === "PORT SCAN"
            ) {

                portScan++;

            } else if (
                type === "BOTNET"
            ) {

                botnet++;

            } else if (
                type === "NORMAL"
            ) {

                normal++;
            }
        }
    );


    const values = [
        ddos,
        portScan,
        botnet,
        normal
    ];


    if (!attackDistributionChart) {

        attackDistributionChart =
            new Chart(
                canvas,
                {

                    type:
                        "doughnut",

                    data: {

                        labels: [

                            "DDoS",

                            "Port Scan",

                            "Botnet",

                            "Normal"
                        ],

                        datasets: [

                            {
                                data:
                                    values
                            }

                        ]
                    },

                    options: {

                        responsive:
                            true,

                        maintainAspectRatio:
                            false
                    }
                }
            );

    } else {

        attackDistributionChart
            .data
            .datasets[0]
            .data = values;


        attackDistributionChart.update(
            "none"
        );
    }
}


// =====================================================
// INCIDENT TABLE
// =====================================================

function updateIncidentTable(
    incidents
) {

    const body =
        getElement(
            "incidentTableBody"
        );


    if (!body) {
        return;
    }


    if (
        incidents.length === 0
    ) {

        body.innerHTML = `
            <tr>
                <td colspan="10">
                    No security incidents detected.
                </td>
            </tr>
        `;

        return;
    }


    body.innerHTML =
        incidents
            .slice(0, 20)
            .map(
                incident => `

                <tr>

                    <td>
                        ${
                            incident.incident_id ||
                            "-"
                        }
                    </td>

                    <td>
                        ${
                            incident.timestamp ||
                            "-"
                        }
                    </td>

                    <td>
                        ${
                            incident.source_ip ||
                            "-"
                        }
                    </td>

                    <td>
                        ${
                            incident.destination_ip ||
                            "-"
                        }
                    </td>

                    <td>
                        ${
                            incident.attack_type ||
                            "-"
                        }
                    </td>

                    <td>
                        ${
                            Math.round(
                                Number(
                                    incident.confidence ||
                                    0
                                ) * 100
                            )
                        }%
                    </td>

                    <td>
                        ${
                            Math.round(
                                Number(
                                    incident.risk_score ||
                                    0
                                )
                            )
                        }
                    </td>

                    <td>
                        ${
                            incident.severity ||
                            "-"
                        }
                    </td>

                    <td>
                        ${
                            incident.recommended_action ||
                            "-"
                        }
                    </td>

                    <td>
                        ${
                            incident.status ||
                            "-"
                        }
                    </td>

                </tr>

            `
            )
            .join("");
}


// =====================================================
// SIMULATOR CONTROLS
// =====================================================

async function startSimulator() {

    await api(
        "/simulator/start",
        {
            method: "POST"
        }
    );

    await updateSimulator();
}


async function stopSimulator() {

    await api(
        "/simulator/stop",
        {
            method: "POST"
        }
    );

    await updateSimulator();
}


async function setAttack(
    attackType
) {

    await api(
        "/simulator/attack/" +
        attackType,
        {
            method: "POST"
        }
    );

    await updateSimulator();
}


// =====================================================
// BUTTONS
// =====================================================

function setupButtons() {

    const startButton =
        getElement(
            "startSimulator"
        );

    if (startButton) {

        startButton.addEventListener(
            "click",
            startSimulator
        );
    }


    const stopButton =
        getElement(
            "stopSimulator"
        );

    if (stopButton) {

        stopButton.addEventListener(
            "click",
            stopSimulator
        );
    }


    const normalButton =
        getElement(
            "normalAttack"
        );

    if (normalButton) {

        normalButton.addEventListener(
            "click",
            () => setAttack("NONE")
        );
    }


    const ddosButton =
        getElement(
            "ddosAttack"
        );

    if (ddosButton) {

        ddosButton.addEventListener(
            "click",
            () => setAttack("DDOS")
        );
    }


    const portScanButton =
        getElement(
            "portScanAttack"
        );

    if (portScanButton) {

        portScanButton.addEventListener(
            "click",
            () => setAttack("PORT_SCAN")
        );
    }


    const botnetButton =
        getElement(
            "botnetAttack"
        );

    if (botnetButton) {

        botnetButton.addEventListener(
            "click",
            () => setAttack("BOTNET")
        );
    }
}


// =====================================================
// START DASHBOARD
// =====================================================

async function initializeDashboard() {

    console.log(
        "6G AI Cyber Defense Dashboard loaded"
    );


    setupButtons();


    await updateSystemStatus();

    await updateSimulator();

    await updateIncidents();


    setInterval(
        updateSystemStatus,
        3000
    );


    setInterval(
        updateSimulator,
        1000
    );


    setInterval(
        updateIncidents,
        3000
    );
}


// =====================================================
// PAGE LOAD
// =====================================================

document.addEventListener(
    "DOMContentLoaded",
    initializeDashboard
);