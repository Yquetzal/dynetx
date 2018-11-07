/**
 * Created by remy on 12/09/16.
 */


function drawNodes(){
    color="Gainsboro"
    name="nodeV"
    console.log(allNodes)
    listOfSequencesOfPoints = allNodes
    console.log("will draw "+Object.keys(listOfSequencesOfPoints).length+"elements "+name);
    svg.selectAll(name)
        .data(d3.values(listOfSequencesOfPoints))
        .enter().append("path")
        .attr("id",name)
        //.style("fill",function (d){return d.color = "rgba(0,0,0,0.0)"; })
        //.style("fill","none")
        .style("stroke",function (d){return d.color = color; })
        //.attr("pointer-events","stroke")
        //.attr("pointer-events",function(d){ if(pointerEvents){return ""}else{return "none"}})
        .attr("d", drawNodeLines)
        //.append("title")
        //.text(function(d) {  return d.name ;})
        .style("cursor", "pointer")
        //.on("drag", drag);
        .call(dragLaunch)
        .style("stroke-width",nodeWidth+"");

	 svg.selectAll(name)
        .data(d3.values(listOfSequencesOfPoints))
        .enter().append("text")
        .attr("x", function(d) { return -40; })
        .attr("y", function(d) { return d.drawCoordinates[0][0].y+0.5*nodeWidth; })
        .text(function (d) { return d.name;})
        .attr("font-family", "sans-serif")
        .attr("font-size", (nodeWidth-1)+" ")
        .attr("fill", "black");
}


/*function drawEdgeProperties(propertyName){
    console.log("edgeProperty: "+propertyName)

    name="edgePropV"

    svg.selectAll("path#"+name)
        .remove();

    listOfSequencesOfPoints = drawObjects[propertyName]
    console.log(listOfSequencesOfPoints)
    //console.log(allNodes)
    //console.log(drawObjects)
    console.log("will draw "+listOfSequencesOfPoints.length+"elements "+name);
    console.log(listOfSequencesOfPoints)
    svg.selectAll(name)
        .data(listOfSequencesOfPoints)
        .enter().append("path")
        .attr("id",name)
        //.style("fill",function (d){return d.color = "rgba(0,0,0,0.0)"; })
        //.style("fill","none")
        //.attr("pointer-events","none")

        .style("stroke",function (d){return d.color; })
        //.attr("pointer-events","stroke")
        //.attr("pointer-events",function(d){ if(pointerEvents){return ""}else{return "none"}})
        .attr("d", function(d){return d.graphic})
        .style("stroke-width","2")
        .on("mouseover", function(d) {
            div.transition()
                .duration(200)
                .style("opacity", .9);
            div	.html("name: "+d.theID + "<br/>"  + "val: "+d.value.toFixed(2)+ "<br/>"  + "dates: "+d.dates)
                .style("left", (d3.event.pageX-20) + "px")
                .style("top", (d3.event.pageY - 65) + "px");
        })
        .on("mouseout", function(d) {
            div.transition()
                .duration(500)
                .style("opacity", 0);
        });

    //.append("title")
    //.text(function(d) {  return d.name ;})
    //.style("cursor", "pointer")
    //.on("drag", drag);
    //.call(dragLaunch);

}
*/

function drawNodeProperties(propertyName){


    name="nodePropV"

    svg.selectAll("path#"+name)
        .remove();

    listOfSequencesOfPoints = drawObjects[propertyName]
    console.log("will draw "+listOfSequencesOfPoints.length+"elements "+name);
    console.log(listOfSequencesOfPoints)

    svg.selectAll(name)
        .data(listOfSequencesOfPoints)
        .enter().append("path")
        .attr("id",name)
        //.style("fill",function (d){return d.color = "rgba(0,0,0,0.0)"; })
        //.style("fill","none")
        //.attr("pointer-events","none")

        .style("stroke",function (d){return d.color; })
        .style("opacity", .6)
        //.attr("pointer-events","stroke")
        //.attr("pointer-events",function(d){ if(pointerEvents){return ""}else{return "none"}})
        .attr("d", function(d){return d.graphic})
        .style("stroke-width",(nodeCommunityWidth)+"")
        .on("mouseover", function(d) {
            div.transition()
                .duration(200)
                .style("opacity", .9);
            div	.html("name: "+d.theID + "<br/>"  + "val: "+d.value+ "<br/>"  + "dates: "+d.dates)
                .style("left", (d3.event.pageX-20) + "px")
                .style("top", (d3.event.pageY - 65) + "px");
        })
        .on("mouseout", function(d) {
            div.transition()
                .duration(500)
                .style("opacity", 0);
        });

    //.append("title")
        //.text(function(d) {  return d.name ;})
        //.style("cursor", "pointer")
        //.on("drag", drag);
        //.call(dragLaunch);

}

/*function drawEdges(){
    name = "edgeV"
    strokeColorr="LightGrey"
    listOfSequencesOfPoints = allEdges
    console.log("will draw "+listOfSequencesOfPoints.length+"elements "+name);
    svg.selectAll(name)
        .data(d3.values(listOfSequencesOfPoints))
        .enter().append("path")
        .attr("id",name)
        //.style("fill",function (d){return d.color = "rgba(0,0,0,0.0)"; })
        .style("fill","none")
        .style("stroke",function (d){return d.color = strokeColorr; })
        //.attr("pointer-events",function(d){ if(pointerEvents){return ""}else{return "none"}})
        .style("stroke-width",2)
        .style("stroke-opacity",0.5)
        .text(function(d) {  return d.name ;})
        .attr("d", function(d){return d.graphic})

}*/

function drawNodeLines(d){
    toReturn = ""
    for (i in d.drawCoordinates){

        toReturn+=nodeToLine(d.drawCoordinates[i])
    }
    //console.log(d.name+" "+toReturn)
    return toReturn
}
var nodeToLine = d3.svg.line()
    .x(function(d) { return d.x; })
    .y(function(d) { return d.y; })
    .interpolate("linear");

var nodeToCurve = d3.svg.line()
    .x(function(d) { return d.x; })
    .y(function(d) { return d.y; })
    .interpolate("basis");


function xNormalization(val,minScale,maxScale,minDisplay,maxDisplay){

	fractionInPossibleRange = (val-minScale)/(maxScale-minScale)
	sizeDisplayedRange = maxDisplay-minDisplay
	convertedInDisplayRange = fractionInPossibleRange*sizeDisplayedRange
	finalPosition = convertedInDisplayRange+minDisplay
	//console.log((val/(maxScale-minScale)*(maxDisplay-minDisplay))+minDisplay)
    return finalPosition
}
function normalizeLStreamX(val){
    return (xNormalization(val,LStream.LSdates[0],LStream.LSdates[1],defaultXNodeLeft,defaultXNodeRight))
}


/*function determineEdgePosition(){
    for (edgeID in allEdges) {
        anEdge = allEdges[edgeID]
        computeEdgePath(anEdge)
    }
}*/


function draw(){
    populateLeftList()
    populateTabLinkFlowProp()

    computeVisualizations()

    drawNodes()
    //drawEdges()
    drawNodeProperties(currentlyDisplayedAttribute)
    //if(detailedEges)
    //    drawEdgeProperties(advancedEdgesPropertiesNames[0])
    console.log("draw objects")
    console.log(drawObjects)
}

function computeVisualizations(){
    determineNodePosition()
    //determineEdgePosition()
    computeNodePropertiesPath(currentlyDisplayedAttribute)
    //if(detailedEges)
    //computeEdgePropertiesPath(advancedEdgesPropertiesNames[0])

}




function plotGraph(){
  time = parseFloat($("#nbNodes").val())
  console.log("pouet");
  console.log(time)
  var G = new jsnx.Graph();

  for (objI in drawObjects["Communities/coms.sgc"]){
    obj =drawObjects["Communities/coms.sgc"][objI]
    dates = obj["dates"]
    dates = dates.split("_")

    if (parseFloat(dates[0])<=time && time<parseFloat(dates[1])){
      G.addNode(obj["theID"],{"color":obj["color"]})//,color=obj["color"]
    }
  }
  console.log("yyy")
  // for (n in allNodes){
  //   for (p in allNodes[n]["periods"]){
  //     period = allNodes[n]["periods"][p]
  //     console.log(period)
  //     console.log(period[0]+" "+period[1]+" "+time)
  //     if (period[0]<=time && time<period[1]){
  //       G.addNode(n)
  //     }
  //   }
  // }

  for (e in allEdges){
    for (p in allEdges[e]["periods"]){
      period = allEdges[e]["periods"][p]
      if (period[0]<=time && time<period[1]){
        G.addEdge(allEdges[e]["endPoints"][0],allEdges[e]["endPoints"][1])
      }
    }
  }
  // for (e in allEdges){
  //   G.addEdge()
  // }
  jsnx.draw(G, {
  element: '#myGraph',
  withLabels: false,
  edgeStyle: {
    'stroke-width': 1,
    fill: '#999'
},
  nodeStyle: {
      fill: function(d) {
          return d.data.color;
      },
      stroke: 'none'

  },
    nodeAttr: {
          r: 5 // default element is circle, so the element will have a radius of 10
      },
  layoutAttr: {
    charge: -200,
    linkDistance: 10
 }
});
}
