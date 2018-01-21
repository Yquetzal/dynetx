/**
 * Created by remy on 12/09/16.
 */


var dragLaunch = d3.behavior.drag() // <-A
    .on("drag", dragmove);

function dragmove(d) {
    console.log(d)
    d.y = d3.event.y
    updateNode(d)
    updateAffectedEdges(d)
    //updateNodeProperties(d.name,"centralities")
    computeNodePropertiesPath(currentlyDisplayedCentrality)

    redraw()
    //d3.select(this).attr("transform", "translate(" + d.x + "," + (d.y = Math.max(0, Math.min(height - d.dy, d3.event.y))) + ")");
    //d3.select(this).attr("transform",
    //link.attr("d", sankey.link());
}


//not optimal, redraw everything every time
function redrawNodes(){
    name="path#nodeV"
    console.log("will redraw nodes");
    svg.selectAll(name)
        .attr("d",  drawNodeLines)

        //.attr("d", function(d){console.log("hiii");console.log(d);return drawNodeLines})


}

//not optimal, redraw everything every time
function redrawEdges(){
    name="path#edgeV"
    console.log("will redraw edges ");
    svg.selectAll(name)
        .attr("d",  function(d){return d.graphic})

    //.attr("d", function(d){console.log("hiii");console.log(d);return drawNodeLines})


}

//not optimal, redraw everything every time
/*function redrawNodeProperties(propertyName){
    name="path#nodePropV"
    console.log("will redraw prop "+propertyName);

    drawNodeProperties(propertyName)

    //svg.selectAll(name)
      //  .attr("d",  drawNodeProperties(propertyName))

    //.attr("d", function(d){console.log("hiii");console.log(d);return drawNodeLines})

}*/


function redraw(){
    redrawNodes()
    redrawEdges()
    drawNodeProperties(currentlyDisplayedCentrality)

    svg.selectAll("path#edgePropV")
        .remove();
    if(detailedEges)
        drawEdgeProperties(advancedEdgesPropertiesNames[0])

}

function displayEdges(){
    detailedEges = true
    redraw()
}
function hideEdges(){
    detailedEges = false
    redraw()
}