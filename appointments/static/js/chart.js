//these chart functions can be combined into one with a conditional switch statement
//it will likely require li's to have a data attr attached

function getId(element) {
    return document.getElementById(element);
}
function chart(event, chartId) {
    //event.preventDefault();
    getId('chartCanvas1').style.display = 'none';
    getId('chartCanvas2').style.display = 'none';
    getId('chartCanvas3').style.display = 'none';
    getId('chartCanvas4').style.display = 'none';
    getId('chartCanvas5').style.display = 'none';

    if (chartId === 1) {
        getId('chartCanvas1').style.display = 'block';
        getChartData(1);
    } else if (chartId === 2) {
        getId('chartCanvas2').style.display = 'block';
        getChartData(2);
    } else if (chartId === 3) {
        getId('chartCanvas3').style.display = 'block';
        getId('chartCanvas4').style.display = 'block';
        getChartData(3);
        getChartData(4);
    } else if (chartId === 4) {
        getId('chartCanvas5').style.display = 'block';
        getChart5Data();
    };
};

///////////Render Charts//////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////

function getChartData(chartId) {
    const records = `/data/records/${chartId}`
    fetch(records)
        .then(response => response.json())
        .then(data => {
            //renderChart1(data)
            const renderChart = `renderChart${chartId}`;
            window[renderChart](data);
        })
}

function getChart5Data() {
    const records = "/data/records/5"
    fetch(records)
        .then(response => response.text())
        .then(html => {
            getId('chartCanvas5').innerHTML = html;
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function renderChart1(da) {
    const ctx = document.getElementById('chartCanvas1');
    console.log(da)
    //get dates from appts api
    //labels = dates. from, to. by day, week, month
    const labels1 = Object.keys(da);
    console.log(Object.keys(da))
    const data1 = Object.values(da);

    new Chart(ctx, {
        type: 'bar',
        data: {
            datasets: [{
                //label: false,
                data: data1,
            }],
            labels: labels1
        },
        options: {
            scales: {
                x: {
                    title: {
                        display: true,
                        //text: 'Date (daily)'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Income (£)'
                    }
                }
            },

            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: 'Daily Income' // Customize the chart title
                }
            }
        }
    });
}


function renderChart2(data2) {
    const ctx = document.getElementById("chartCanvas2");
    const dateLabels = Object.keys(data2)
    const aggEarnings = Object.values(data2)

    const data = {
        labels: dateLabels,
        datasets: [{
            //label: 'Total Aggregate Income to Date',
            data: aggEarnings,
            fill: false,
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1
        }]
    };

    const config = {
        type: 'line',
        data: data,
        options: {
            scales: {
                x: {
                    title: {
                        display: true,
                        //text: 'Date (weekly)'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Gross Income (£)'
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: 'Aggregate Income by Week' // Customize the chart title
                }
            }
        }
    };
    const chart = new Chart(ctx, config);
}



function renderChart3(data3) {
    const ctx = document.getElementById("chartCanvas3")
    const aptTypes = Object.keys(data3)//list of apt types
    const aptTypesByNumber = Object.values(data3)//list of numbers for each

    const data = {
        labels: aptTypes,
        datasets: [{
            label: 'Popularity of Appointment by Type',
            data: aptTypesByNumber,
            backgroundColor: [
                'rgba(247, 155, 219, 0.5)',
                'rgba(183, 94, 156, 0.5)',
                'rgba(112, 17, 84, 0.5)'
            ],
            hoverOffset: 4
        }]
    };

    const config = {
        type: 'doughnut',
        data: data,
        options: {
            plugins: {
                title: {
                    display: true,
                    text: 'Popularity of Appointment by Type'
                }
            }
        }
    };

    const chart = new Chart(ctx, config);
}


function renderChart4(data4) {
    const ctx = document.getElementById("chartCanvas4")
    const aptTypes = Object.keys(data4)//list of apt types
    const aptTypesEarnings = Object.values(data4)//list of numbers for each

    const data = {
        labels: aptTypes,
        datasets: [{
            label: 'Total Income by Appointment Type',
            data: aptTypesEarnings,
            backgroundColor: [
                'rgba(0, 98, 26, 0.5)',
                'rgba(39, 146, 68, 0.5)',
                'rgba(115, 210, 141, 0.5)'
            ],
            hoverOffset: 4
        }]
    };

    const config = {
        type: 'doughnut',
        data: data,
        options: {
            plugins: {
                title: {
                    display: true,
                    text: 'Total Income by Appointment Type'
                }
            }
        }
    };

    const chart = new Chart(ctx, config);
}

// Resize chart based on screen size
function resizeChart() {
    const chartContainer = document.getElementById('chartContainer');
    const scrWidth = window.innerWidth;
    if (scrWidth < 500) {
        document.querySelector(".advice").style.display = 'block';
    } else {
        document.querySelector(".advice").style.display = 'none';
    }
}

// Call the resizeChart function initially


// Call the resizeChart function on window resize
window.addEventListener('resize', resizeChart);

document.addEventListener('DOMContentLoaded', () => {
    chart(1);
    const trigger1 = document.getElementById("income-li");
    trigger1.addEventListener("click", event => {
        chart(event, 1)
    });

    const trigger2 = document.getElementById("total-li");
    trigger2.addEventListener("click", event => {
        chart(event, 2)
    });
    const trigger3 = document.getElementById("appointments-li");
    trigger3.addEventListener("click", event => {
        chart(event, 3)
    });

    const trigger4 = document.getElementById("tax-li");
    trigger4.addEventListener("click", event => {
        chart(event, 4)
    });
    resizeChart();
    chart(1, 1)
}
)

//277 lines of code on 6 jun 23


/*


function renderChart(chartId, data1) {
    const ctx = document.getElementById("chartCanvas3")
    const aptTypes = Object.keys(data1)//list of apt types
    const recordData = Object.values(data1)//list of numbers for each

    if (chartId === 1) {
        legend = 'false';
        textContent = 'Daily Income in £'
        graphType = 'bar';
        colours = null;
    } else if (chartId === 2) {
        legend = 'false';
        textContent = 'Aggregate Income by Week'
        graphType = 'line';
        colours = null;
    } else if (chartId === 3 || 4) {
        legend = true;
        textContent = 'Popularity of Appointment by Type'
        graphType = 'doughnut'
        colours = [
            'rgba(247, 155, 219, 0.5)',
            'rgba(183, 94, 156, 0.5)',
            'rgba(112, 17, 84, 0.5)'
        ];
    } else if (chartId === 4) {
        textContent = 'Total Income by Appointment Type'
        colours = [
            'rgba(0, 98, 26, 0.5)',
            'rgba(39, 146, 68, 0.5)',
            'rgba(115, 210, 141, 0.5)'
        ]
    };

    const dataFeed = {
        labels: aptTypes,
        datasets: [{
            label: textContent,
            data: recordData,
            backgroundColor: colours,
        }]
    };

    const config = {
        type: graphType,
        data: dataFeed,
        options: {
            plugins: {
                legend: {
                    display: legend
                },
                title: {
                    display: true,
                    text: textContent
                }
            }
        }
    };

    const chart = new Chart(ctx, config);
}*/