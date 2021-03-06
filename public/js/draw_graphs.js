var width = 960;
var height = 600;
var margin = 20;
var padding = margin / 2;
var color = d3.scale.category20();

// Generates a tooltip for a SVG circle element based on its ID
function addTooltip(circle, analysisType) {
    var x = parseFloat(circle.attr("cx"));
    var y = parseFloat(circle.attr("cy"));
    var r = parseFloat(circle.attr("r"));
    var text = circle.attr("id");
    var tooltip = d3.select("#plot"+analysisType)
        .append("text")
        .text(text)
        .attr("x", x)
        .attr("y", y)
        .attr("dy", -r * 2)
        .attr("id", "tooltip");
    var offset = tooltip.node().getBBox().width / 2;
    if ((x - offset) < 0) {
        tooltip.attr("text-anchor", "start");
        tooltip.attr("dx", -r);
    }
    else if ((x + offset) > (width - margin)) {
        tooltip.attr("text-anchor", "end");
        tooltip.attr("dx", r);
    }
    else {
        tooltip.attr("text-anchor", "middle");
        tooltip.attr("dx", 0);
    }
}

var vis = d3.select("#chart")
    .append("svg:svg")
    .attr("width", width)
    .attr("height", height)
    .attr("pointer-events", "all")
    .append('svg:g')
    .call(d3.behavior.zoom().on("zoom", redraw))
    .append('svg:g');

vis.append('svg:rect')
    .attr('width', width)
    .attr('height', height)
    .attr('fill', 'white');

function redraw() {
    vis.attr("transform",
        "translate(" + d3.event.translate + ")"
        + " scale(" + d3.event.scale + ")");
}

function tick(e) {
    // Push different nodes in different directions for clustering.
    var k = 6 * e.alpha;
    graph.nodes.forEach(function (o, i) {
        o.y += i & 1 ? k : -k;
        o.x += i & 2 ? k : -k;
    });
    node.attr("cx", function (d) { return d.x; })
        .attr("cy", function (d) { return d.y; });
}
// Draws nodes on plot
function drawNodes(nodes, analysisType) {
    // used to assign nodes color by community
    var color = d3.scale.category20();
    d3.select("#plot"+analysisType).selectAll(".node")
        .data(nodes)
        .enter()
        .append("circle")
        .attr("class", "node")
        .attr("id", function (d, i) { return d.domain; })
        .attr("cx", function (d, i) { return d.x; })
        .attr("cy", function (d, i) { return d.y; })
        .attr("r", function (d, i) { 
            return (analysisType == "pagerank") ? d.pagerank : 4;
        })
        .style("fill", function (d, i) { return color(d.community); })
        .on("mouseover", function (d, i) { addTooltip(d3.select(this), analysisType); })
        .on("mouseout", function (d, i) { d3.select("#tooltip").remove(); });
}
// Draws edges between nodes
function drawEdges(links, analysisType) {
    var scale = d3.scale.linear()
        .domain(d3.extent(links, function (d, i) {
            return d.value;
        }))
        .range([1, 6]);
    d3.select("#plot"+analysisType).selectAll(".link")
        .data(links)
        .enter()
        .append("line")
        .attr("class", "link")
        .attr("x1", function (d) { return d.source.x; })
        .attr("y1", function (d) { return d.source.y; })
        .attr("x2", function (d) { return d.target.x; })
        .attr("y2", function (d) { return d.target.y; })
        .style("stroke-width", function (d, i) {
            return scale(d.value) + "px";
        })
        .style("stroke-dasharray", function (d, i) {
            return (d.value <= 1) ? "2, 2" : "none";
        });
}

function drawGraph(graph, analysisType) {
    var svg = d3.select("#" + analysisType).append("svg")
        .attr("width", width)
        .attr("height", height);

    // draw plot background
    svg.append("rect")
        .attr("width", width)
        .attr("height", height)
        .style("fill", "#f6f6f6");
    // create an area within svg for plotting graph
    var plot = svg.append("g")
        .attr("id", "plot"+analysisType)
        .attr("transform", "translate(" + padding + ", " + padding + ")");
    var layout = d3.layout.force()
        .size([width - margin, height - margin])
        .charge(-10)
        .linkDistance(function (d, i) {
            return (d.source.community == d.target.community) ? 30 : 60;
        })
        .nodes(graph.nodes)
        .links(graph.links)
        .start();
    drawEdges(graph.links, analysisType);
    drawNodes(graph.nodes, analysisType);
    // drag and update layout
    d3.selectAll(".node").call(layout.drag);
    layout.on("tick", function () {
        d3.selectAll(".link")
            .attr("x1", function (d) {
                return d.source.x;
            })
            .attr("y1", function (d) {
                return d.source.y;
            })
            .attr("x2", function (d) {
                return d.target.x;
            })
            .attr("y2", function (d) {
                return d.target.y;
            });
        d3.selectAll(".node")
            .attr("cx", function (d) {
                return d.x;
            })
            .attr("cy", function (d) {
                return d.y;
            });
    });
}

function drawLPAGraph(graph) {
    drawGraph(graph, "lpa")
}

function drawPagerankGraph(data) {
    var radius = Math.min(width, height) / 2 - 20;
    var color = d3.scale.ordinal()
        .range(["#98abc5", "#8a89a6", "#7b6888", "#6b486b", "#e5aab6", "#a05d56", "#d0743c", "#ff8c00", "#dfac84", "#b36200"]);
    var arc = d3.svg.arc()
        .outerRadius(radius - 10)
        .innerRadius(radius - 70);
    var pie = d3.layout.pie()
        .sort(null)
        .value(function (d) {
            return d.pagerank;
        });
    var svg = d3.select("#pagerank").append("svg")
        .attr("width", width)
        .attr("height", height)
        .append("g")
        .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

    var g = svg.selectAll(".arc")
        .data(pie(data))
        .enter().append("g")
        .attr("class", "arc");
    g.append("path")
        .attr("d", arc)
        .style("fill", function (d) {
            return color(d.data.name);
        });
    g.append("text")
        .attr("transform", function (d) {
            return "translate(" + arc.centroid(d) + ")";
        })
        .attr("dy", ".35em")
        .text(function (d) {
            return Math.round(d.data.pagerank, 2);
        });

    svg.append("text")
        .attr("dy", ".35em")
        .style("text-anchor", "middle")
        .text(function (d) {
            return "Top 10 websites";
        });

    var legend = d3.select("#pagerank").append("svg")
        .attr("class", "legend")
        .attr("width", radius * 2)
        .attr("height", radius * 2)
        .selectAll("g")
        .data(color.domain().slice().reverse())
        .enter().append("g")
        .attr("transform", function (d, i) {
            return "translate(0," + i * 20 + ")";
        });

    legend.append("rect")
        .attr("width", 18)
        .attr("height", 18)
        .style("fill", color);

    legend.append("text")
        .attr("x", 24)
        .attr("y", 9)
        .attr("dy", ".35em")
        .text(function (d) {
            return d;
        });
}