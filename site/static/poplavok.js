function fillHeader(data) {
    $('#server_time').html(data['server_time']);
    $('#current_series').html(data['current_series']);
    $('#current_calibration').html(data['current_calibration']);
    $('#device_status').html(data['device_status']);
    $('#fanSpeed').html(data['fanSpeed']);
    $('#temperature').html(data['lastTemp']);
    $('#pressure').html(data['lastPres']);
    $('#r_humidity').html(data['lastRHum']);
    $('#a_humidity').html(data['lastAHum']);
    $('#ppmM_H2O').html(data['lastH2OppmM']);
    $('#ppmV_H2O').html(data['lastH2OppmV']);
    $('#last_time').html(data['lastTime']);
    $('#voltage').html(data['lastVolt']);
    $('#CH4').html(data['lastCH4']);
};

var statusBufferSize = 100;
var statusBuffer = []
function updateStatusBuffer(data) {
    if (localStorage['statusBuffer'])
    {
        statusBuffer = JSON.parse(localStorage.getItem('statusBuffer'));
    }

    if (statusBuffer.length > statusBufferSize) {
        statusBuffer.shift();
    }    
    statusBuffer.push(data);

    localStorage.setItem('statusBuffer', JSON.stringify(statusBuffer));
}

function clearStatusBuffer()
{
    statusBuffer = [];
    localStorage.setItem('statusBuffer', JSON.stringify(statusBuffer));
}

function refresh(url) {
    $.ajax({
        url: url,
        success: function (data) {
            fillHeader(data);
            updateStatusBuffer(data);
        },
    });
};

function setFansSpeed(speed) {
    $.ajax({
        url: `setFansSpeed/${speed}`,
        success: function (data) {
            fan_slider = document.getElementById('rangeValue')
            if (data['status'] == 0) {
                speed = 0
            }
            fan_slider.innerHTML = speed + '%'
        }
    })
}

function updatePlot(valueName) {
    var timeArray = statusBuffer.map((d) => new Date(d['lastTime']));
    var dataArray = statusBuffer.map((d) => parseFloat(d[valueName]));

    var layout = {
        xaxis: {
            range: [timeArray[0], timeArray.slice(-1)],
            ticks: 'outside'
        },
        title: plotValue
    };
    var data = [{
        x: timeArray,
        y: dataArray,
        mode: 'markers'
    }];
    Plotly.newPlot("myPlot", data, layout, { staticPlot: true });
}

function selectPlotValue(element) {
    plotValue = element.textContent;
}