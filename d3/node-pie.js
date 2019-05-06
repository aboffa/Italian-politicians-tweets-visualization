// Thanks to:  https://bl.ocks.org/kgeorgiou
// Source: https://bl.ocks.org/kgeorgiou/68f864364f277720252d0329408433ae#node-pie.js

var DEFAULT_OPTIONS = {
    radius: 20,
    outerStrokeWidth: 10,
    parentNodeColor: 'blue',
    showPieChartBorder: true,
    pieChartBorderColor: 'white',
    pieChartBorderWidth: '2',
    showLabelText: false,
    labelText: 'text',
    labelColor: 'blue'
};

function getOptionOrDefault(key, options, defaultOptions) {
    defaultOptions = defaultOptions || DEFAULT_OPTIONS;
    if (options && key in options) {
        return options[key];
    }
    return defaultOptions[key];
}

function drawParentCircle(nodeElement, options) {
    var outerStrokeWidth = getOptionOrDefault('outerStrokeWidth', options);
    var radius = getOptionOrDefault('radius', options);
    var parentNodeColor = getOptionOrDefault('parentNodeColor', options);

    nodeElement.insert("circle")
        .attr("id", "parent-pie")
        .attr("r", radius)
        .attr("fill", function (d) {
            return parentNodeColor;
        })
        .attr("stroke", function (d) {
            return parentNodeColor;
        })
        .attr("stroke-width", outerStrokeWidth);
}

function drawPieChartBorder(nodeElement, options) {
    var radius = getOptionOrDefault('radius', options);
    var pieChartBorderColor = getOptionOrDefault('pieChartBorderColor', options);
    var pieChartBorderWidth = getOptionOrDefault('pieChartBorderWidth', options);

    nodeElement.insert("circle")
        .attr("r", radius)
        .attr("fill", 'transparent')
        .attr("stroke", pieChartBorderColor)
        .attr("stroke-width", pieChartBorderWidth);
}

function drawPieChart(nodeElement, percentages, options) {
    console.log(percentages)
    var radius = getOptionOrDefault('radius', options);
    var halfRadius = radius / 2;
    var halfCircumference = 2 * Math.PI * halfRadius;

    var percentToDraw = 0;
    for (var p in percentages) {
        percentToDraw += percentages[p].percent;

        var toRotate = (180-(1.8 *  percentages[0].percent ))
        nodeElement.insert('circle', '#parent-pie + *')
            .attr("r", halfRadius)
            .attr("fill", 'transparent')
            .style('stroke',percentages[p].color)
            .style('stroke-width', radius)
            .style('stroke-dasharray',
                halfCircumference * percentToDraw / 100
                + ' '
                + halfCircumference)
            //.attr("transform","rotate("+radius+","+radius+","+toRotate+")");
            .attr("transform","rotate("+toRotate+")");
    }
/*

    var k = percentages[0] /100
    var r = radius
    var t0, t1 = k * 2 * Math.PI;

    // Solve for theta numerically.
    if (k > 0 && k < 1) {
        t1 = Math.pow(12 * k * Math.PI, 1 / 3);
        for (var i = 0; i < 10; ++i) {
            t0 = t1;
            t1 = (Math.sin(t0) - t0 * Math.cos(t0) + 2 * k * Math.PI) / (1 - Math.cos(t0));
        }
        k = (1 - Math.cos(t1 / 2)) / 2;
    }

    var h = 2 * r * k,
        y = r - h,
        a = (Math.PI - t1) / 2;

    var clip = d3.select("#clip rect");

    clip
        .attr("y", y)
        .attr("height", h);


    nodeElement.insert('circle')
        .attr("fill", "steelblue")
        .attr("clip-path", "url(#clip)")
        .attr("r", halfRadius)

    nodeElement.insert('circle')
        .attr("fill", "none")
        .attr("stroke","black")
        .attr("clip-path", "url(#clip)")
        .attr("r", halfRadius)
*/
}

function drawTitleText(nodeElement, options) {
    var radius = getOptionOrDefault('radius', options);
    var text = getOptionOrDefault('labelText', options);
    var color = getOptionOrDefault('labelColor', options);

    nodeElement.append("text")
        .text(String(text))
        .attr("fill", color)
        .attr("dy", radius + 20);
}

var NodePieBuilder = {
    drawNodePie: function (nodeElement, percentages, options) {
        drawParentCircle(nodeElement, options);

        if (!percentages) return;
        drawPieChart(nodeElement, percentages, options);

        var showPieChartBorder = getOptionOrDefault('showPieChartBorder', options);
        if (showPieChartBorder) {
            drawPieChartBorder(nodeElement, options);
        }

        var showLabelText = getOptionOrDefault('showLabelText', options);
        if (showLabelText) {
            drawTitleText(nodeElement, options);
        }
    }
};