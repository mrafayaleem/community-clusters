var width = 960;
var height = 600;

var svg = d3.select("#lpa").append("svg")
    .attr("width", width)
    .attr("height", height);

var color = d3.scaleOrdinal(d3.schemeCategory20);

function drawLPAGraph(graph){
    var simulation = d3.forceSimulation(graph.nodes)
        .force("link", d3.forceLink().id(function (d) {
            return d.id;
        }))
        .force("charge", d3.forceManyBody())
        .force("center", d3.forceCenter(width / 2, height / 2))
        .stop();

        
    simulation.force("link").links(graph.links);

    // for (var i = 0; i < 300; ++i)
    //     simulation.tick();

    // var link = svg.append("g")
    //     .attr("class", "links")
    //     .selectAll("line")
    //     .data(graph.links)
    //     .enter().append("line")
    //     .attr("x1", function (d) {
    //         return d.source.x;
    //     })
    //     .attr("y1", function (d) {
    //         return d.source.y;
    //     })
    //     .attr("x2", function (d) {
    //         return d.target.x;
    //     })
    //     .attr("y2", function (d) {
    //         return d.target.y;
    //     })
    //     .attr("stroke-width", function (d) {
    //         return Math.sqrt(d.value);
    //     });

    // var node = svg.append("g")
    //     .attr("class", "nodes")
    //     .selectAll("circle")
    //     .data(graph.nodes)
    //     .enter().append("circle")
    //     .attr("cx", function (d) {
    //         return d.x;
    //     })
    //     .attr("cy", function (d) {
    //         return d.y;
    //     })
    //     .attr("r", 5)
    //     .attr("fill", function (d) {
    //         return color(d.group);
    //     })
    //     .call(d3.drag()
    //         .on("start", dragstarted)
    //         .on("drag", dragged)
    //         .on("end", dragended));

    // node.append("title")
    //     .text(function (d) {
    //         return d.id;
    //     });

}

function dragstarted(d) {
    if (!d3.event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
}

function dragged(d) {
    d.fx = d3.event.x;
    d.fy = d3.event.y;
}

function dragended(d) {
    if (!d3.event.active) simulation.alphaTarget(0);
    d.fx = null;
    d.fy = null;
}