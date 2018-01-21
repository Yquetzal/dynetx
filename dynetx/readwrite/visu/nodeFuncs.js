/**
 * Created by remy on 13/09/16.
 */

function determineNodePosition(){
    //nodeInd = 0
    for (nodeID in allNodes) {
        aNode = allNodes[nodeID]
        thisY = firstNodeY + nodeOrder.indexOf(nodeID) * distanceBetweenNodes
        aNode.drawCoordinates = []
        aNode.y = thisY
        updateNode(aNode)

        //nodeInd+=1
    }
}

function updateNode(n){
    console.log("updating: "+n)
    n.drawCoordinates = []
    for (periodI in n.periods) {

        x1 = normalizeLStreamX(n.periods[periodI][0])
        x2 = normalizeLStreamX(n.periods[periodI][1])
        n.drawCoordinates.push([{"x": x1, "y": n.y}, {"x": x2, "y": n.y}])
    }
    //console.log(n.drawCoordinates)
}

function updateAffectedEdges(nod){
    for(i in allEdges){
        edge = allEdges[i]
        if( edge.endPoints.indexOf(nod.name )> -1){
            computeEdgePath(edge)
        }
    }
}

/*function redScale(val,max){

    scale = ['#ffffe0', '#fff2c7', '#ffe5b1', '#ffd79d', '#ffc88e', '#ffba81', '#ffaa76', '#ff9a6e', '#fc8968', '#f77b63', '#f16b5f', '#e95d5a', '#e24f55', '#d8414e', '#cd3346', '#c3263d', '#b61932', '#a90c25', '#9a0316', '#8b0000']
    color = scale[Math.round(val/max*(scale.length-1))]
    return color
    //return "rgb("+255-(255/max*val)+",0,0)"
}*/

function computeNodePropertiesPath(propertyName){
    maxVal = 0
    for(i in allNodes) {
        for(period in allNodes[i][propertyName]){
            maxVal = Math.max(maxVal,allNodes[i][propertyName][period])
        }
        //maxVal = Math.max(maxVal,Math.max.apply(null,allNodes[i][propertyName]))
    }
    drawObjects[propertyName+"Max"] = maxVal
    drawObjects[propertyName]=[]
    //anEdge[propertyName+"_graphic"] = ""
    
    
    //build color scale
    allCommunities = new Set()
    for (n in allNodes){
    	for(period in allNodes[n][propertyName]){
    		allCommunities.add(allNodes[n][propertyName][period])
    	}
    }
    allCommunities = Array.from(allCommunities)
    allCommunities.sort()
    console.log(allCommunities)
    
    for(n in allNodes){
        updateNodeProperties(allNodes[n],propertyName,allCommunities)

    }
}

/*function updateNodeProperties(n,propertyName){
    //console.log("check n for "+propertyName)
    //console.log(n)
    for (t=0;t<LStream[propertyName].length-1;t++) {
        startP = LStream[propertyName][t]
        endP = LStream[propertyName][t + 1]
        thisY = n.y
        x1 = normalizeLStreamX(startP)
        x2 = normalizeLStreamX(endP)
        lineToDraw = nodeToLine([{"x": x1, "y": thisY}, {"x": x2, "y": thisY}])
        if (n[propertyName][t] > 0) {
            drawObjects[propertyName].push({
                "graphic": lineToDraw,
                "color": redScale(n[propertyName][t], drawObjects[propertyName+"Max"]),
                "nodeID":n.name,
                "value":n[propertyName][t]
            })
        }
    }
}*/

function updateNodeProperties(n,propertyName,allCommunities){
    //comColorScale = d3.schemeCategory20b
    var comColorScale = d3.scale.category20().domain(d3.range(0,20));

    //console.log(comColorScale)
    //console.log(comColorScale(0))

    //console.log("check n for "+propertyName)
    //console.log(n)
    for(IDperiod in n[propertyName]) {
        //console.log(startEnd = n[propertyName][IDperiod])

        startEnd = IDperiod.split("_")
        startP = parseFloat(startEnd[0])
        endP = parseFloat(startEnd[1])

        thisY = n.y
        x1 = normalizeLStreamX(startP)
        x2 = normalizeLStreamX(endP)
        lineToDraw = nodeToLine([{"x": x1, "y": thisY}, {"x": x2, "y": thisY}])

        //if (n[propertyName][IDperiod] > 0) {
            //aColor = redScale(n[propertyName][IDperiod], drawObjects[propertyName + "Max"])
            //if (propertyName.indexOf("comm") !== -1){
                //console.log([n[propertyName][IDperiod]%20)
            aColor = comColorScale(allCommunities.indexOf(n[propertyName][IDperiod])%20)
            console.log(n[propertyName][IDperiod])

            console.log(aColor)
            //}
            //console.log(aColor)
            drawObjects[propertyName].push({
                "graphic": lineToDraw,
                "color": aColor,
                "theID": n.name,
                "value": n[propertyName][IDperiod],
                "dates":IDperiod
            })
        //}
    }
}