const ctx = document.getElementById("sensorChart").getContext("2d");
const initialDate = '2025-03-01';
let sensorChart = new Chart(ctx, {
    type: "line",
    data: {
        labels: [],
        datasets: [{
            label: "Temperature (°C)",
            borderColor: "red",
            backgroundColor: "rgba(255, 0, 0, 0.2)",
            data: []
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            x: {
                type: "time", // Use time scale for timestamps
                time: {
                    parser: "yyyy-MM-dd HH:mm:ss", // Ensure format matches CSV
                    tooltipFormat: "yyyy-MM-dd HH:mm:ss",
                    unit: "hour", // Adjust based on data frequency
                    displayFormats: {
                        second: "HH:mm:ss",
                        minute: "HH:mm",
                        hour: "HH:mm",
                        day: "yyyy-MM-dd"
                    }
                },
                min: new Date(initialDate).setHours(0, 0, 0, 0),
                max: new Date(initialDate).setHours(23, 59, 59, 999),
                title: {
                    display: true,
                    text: "Time"
                }
            },
            y: {
                title: {
                    display: true,
                    text: "Temperature (°C)"
                },
                suggestedMin: 15,
                suggestedMax: 40
            }
        }
    }
});

// Function to fetch and update graph for a selected date
function fetchDataByDate() {
    let selectedDate = document.getElementById("date-picker").value || initialDate;
    if (!selectedDate) {
        alert("Please select a date.");
        return;
    }
    // Set x-axis min and max to cover the full day
    let startOfDay = new Date(selectedDate).setHours(0, 0, 0, 0);
    let endOfDay = new Date(selectedDate).setHours(23, 59, 59, 999);
    sensorChart.options.scales.x.min = startOfDay;
    sensorChart.options.scales.x.max = endOfDay;
    
    // Function to Fetch and Update Graph
    fetch(`/data?date=${selectedDate}`)  // Fetch CSV data from ESP32
        .then(response => response.text())  // Convert response to text
        .then(csvText => {
            console.log("CSV Data Received:", csvText); // Debugging output

            let lines = csvText.trim().split("\n");
            let labels = [], temperatures = [];

            lines.forEach(line => {
                let parts = line.split(",");
                if (parts.length === 2) {
                    let timestamp = parts[0].trim();
                    let temperature = parseFloat(parts[1].trim());
                    
                    // Convert timestamp to Date object
                    let dateObj = new Date(timestamp);

                    console.log("Parsed:", dateObj, temperature); // Debugging output

                    labels.push(dateObj);
                    temperatures.push(temperature);  // Store temperature
                }
            });
            
            // Clear existing data
            sensorChart.data.labels = [];
            sensorChart.data.datasets.forEach(dataset => {
                dataset.data = [];
            });
            
            // Update graph with new data
            sensorChart.data.labels = labels;
            sensorChart.data.datasets[0].data = temperatures;
            sensorChart.update();
        })
        .catch(error => console.error("Error fetching data:", error));
}

// Set the date picker to today's date
function setDefaultDate() {
    document.getElementById("date-picker").value = initialDate;
}

// Set default date on page load and fetch data for today
document.addEventListener("DOMContentLoaded", () => {
    setDefaultDate();
    fetchDataByDate();
});

// Ensure function is globally accessible
window.fetchDataByDate = fetchDataByDate;

// Refresh graph every 16 seconds
setInterval(updateGraph, 16000);
updateGraph();  // Initial call to populate the graph
