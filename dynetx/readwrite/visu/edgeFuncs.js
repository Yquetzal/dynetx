/**
 * Created by remy on 28/10/16.
 */
function computeEdgePropertiesPath(propertyName){
    maxVal = 0
    for(i in allEdges) {
        for(period in allEdges[i][propertyName]){
            maxVal = Math.max(maxVal,allEdges[i][propertyName][period])
        }
        //maxVal = Math.max(maxVal,Math.max.apply(null,allNodes[i][propertyName]))
    }
    drawObjects[propertyName+"Max"] = maxVal
    drawObjects[propertyName]=[]
    //anEdge[propertyName+"_graphic"] = ""
    for(n in allEdges){
        updateEdgeProperties(allEdges[n],propertyName)

    }
}

function updateEdgeProperties(n,propertyName){
    console.log("check n for "+propertyName)
    console.log(n)
    for(IDperiod in n[propertyName]) {
        //console.log(startEnd = n[propertyName][IDperiod])

        startEnd = IDperiod.split("_")
        startP = parseFloat(startEnd[0])
        endP = parseFloat(startEnd[1])


        thisY = n.y
        x1 = normalizeLStreamX(startP)
        x2 = normalizeLStreamX(endP)
        lineToDraw = createEdgeShape(n,x1,x2)
        if (n[propertyName][IDperiod] > 0) {
            drawObjects[propertyName].push({
                "graphic": lineToDraw.graphic,
                "color": redScale(n[propertyName][IDperiod], drawObjects[propertyName + "Max"]),
                "theID": n.endPoints[0]+"_"+n.endPoints[1],
                "value": n[propertyName][IDperiod],
                "dates":IDperiod
            })
        }
    }
}




function createEdgeShape(anEdge,x1,x2){
    extremities = [allNodes[anEdge.endPoints[0]],allNodes[anEdge.endPoints[1]]]
    thisY = (extremities[0].y + extremities[1].y)/2
    thisY = thisY - 0.1 * (extremities[1].y-extremities[0].y)
    toReturn ={}
    toReturn.y=thisY
    toReturn.graphic = ""
    //for (periodI in anEdge.periods) {
    //x1 = normalizeLStreamX(anEdge.periods[periodI][0])
    //x2 = normalizeLStreamX(anEdge.periods[periodI][1])
    toReturn.graphic += nodeToLine([{"x": x1 + 0, "y": thisY}, {"x": x2, "y": thisY}])
    toReturn.graphic += nodeToCurve([{"x": x1, "y": extremities[0].y}, {"x": x1 + 2, "y": thisY}, {
        "x": x1,
        "y": extremities[1].y
    }])
    //}
    return toReturn

}
function computeEdgePath(anEdge){
/*    extremities = [allNodes[anEdge.endPoints[0]],allNodes[anEdge.endPoints[1]]]
    thisY = (extremities[0].y + extremities[1].y)/2
    thisY = thisY - 0.1 * (extremities[1].y-extremities[0].y)
    anEdge.y=thisY
    anEdge.graphic = "" */
    anEdge.graphic = ""
    for (periodI in anEdge.periods) {
        x1 = normalizeLStreamX(anEdge.periods[periodI][0])
        x2 = normalizeLStreamX(anEdge.periods[periodI][1])
        theShape = createEdgeShape(anEdge,x1,x2)
        anEdge.y = theShape.y
        anEdge.graphic += theShape.graphic
        //anEdge.graphic+=nodeToLine([{"x": x1+0, "y": thisY}, {"x": x2, "y": thisY}])
        //anEdge.graphic+=nodeToCurve([{"x": x1, "y": extremities[0].y},{"x": x1+2, "y": thisY}, {"x": x1, "y": extremities[1].y}])
    }

}