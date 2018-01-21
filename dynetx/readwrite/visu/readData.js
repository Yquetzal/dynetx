/**
 * Created by remy on 12/09/16.
 */

var functionsFinished = []
function asyncronousFunctionEnded( name){
    functionsFinished.push(name);
    if(functionsFinished.length==1){
        //loadLSproperties(fileProperties)
        //for(i in pathCentralities) {
         //   loadNodeStat(pathCentralities[i], possibleNodeAttributes[i])
        //}
        for(i in advancedPropertyPaths) {
            loadNodeExplicitStat(advancedPropertyPaths[i], advancedPropertiesNames[i])
        }

        //for(i in advancedEdgesPropertiesPaths){
        //    loadEdgeExplicitStat(advancedEdgesPropertiesPaths[i], advancedEdgesPropertiesNames[i])
        //}
        //loadNodeExplicitStat(advancedPropertyFile,advancedPropertyNames)
        loadNodeOrder(fileNodeOrder)
        //loadStationWeights(fileWeights,"weightsRef","weightsNames");
        //loadStationWeights(fileWeights2,"weightsToCompare","secondWeightsNames");
        //loadEdgesWeights();
    }
    console.log("HERE "+functionsFinished.length+" / "+(1+advancedPropertyPaths.length))
    if(functionsFinished.length==2+advancedPropertyPaths.length){
        //console.log("cici"+weightsNames)
        //console.log("cici"+secondWeightsNames)
        console.log("finished to load files")
		possibleNodeAttributes = []
        possibleNodeAttributes = possibleNodeAttributes.concat(advancedPropertiesNames)
        draw();
        functionsFinished=[] ;

        console.log("drawn")
    }
}


function loadNetwork(fileNet){

    console.log("starting loading nodes")

    $.get(fileNet, function(response) {
        //var options={"separator":","}
        var lines = $.csv.toArrays(response,{"separator":"\t"})
        //console.log(lines)
        for(var iL in lines) {
            line = lines[iL]
            //console.log(line)
            if (line[0] == "LS") {
                LSdates = [parseFloat(line[1]), parseFloat(line[2])]
                LStream.LSdates = LSdates
            }
            if (line[0] == "N"){

                name = line[1]
                periods = []
                for (i=0;i<(line.length - 2)/2;i++) {
                    periods.push([parseFloat(line[i * 2 + 2]), parseFloat(line[i * 2 + 3])])
                }
                allNodes[name]={"name":name, "periods":periods}
            }
            if (line[0]=="E") {
                endPoints = [line[1], line[2]]
                edgeID = line[1]+"_"+line[2]
                periods = []
                for(i=0;i<(line.length - 3)/2;i++) {
                    periods.push([parseFloat(line[i * 2 + 3]), parseFloat(line[i * 2 + 4])])
                }
                allEdges[edgeID] ={"endPoints":endPoints, "periods":periods}

            }
        }
        console.log("all loaded nodes:")
        console.log(allNodes)
        //console.log(allEdges)
        asyncronousFunctionEnded("loadStations");
    },"text")

}

function arrayToFloat(array){
    arrayFloat = array.map(function (x) {
        return parseFloat(x);
    });
    return arrayFloat
}

/*function loadNodeStat(fileToRead,propertyName){
    console.log("starting loading "+fileToRead)

    $.get(fileToRead, function(response) {

        //var options={"separator":","}
        var lines = $.csv.toArrays(response,{"separator":"\t"})
        firstLine = lines.shift()
        synchronizedPeriod=firstLine.slice(1,firstLine.length)

        for(var iL in lines) {
            line = lines[iL]
            node = line[0]
            allNodes[node][propertyName]=[]
            for(p=1;p<line.length;p++) {
                allNodes[node][propertyName][synchronizedPeriod[p]] = parseFloat(line[p])
            }
            //allNodes[node][propertyName] = arrayToFloat(allNodes[node][propertyName])
        }

        asyncronousFunctionEnded(propertyName);
    },"text").fail(function() {
        console.log("file not found: "+fileToRead)

        LStream[propertyName]=[]
        for (node in allNodes){
            allNodes[node][propertyName]=[]
        }
        asyncronousFunctionEnded(propertyName);
        //console.log("oups")
        //alert("woops");
    });

}*/


/*function loadEdgeExplicitStat(fileToRead,propertyName){
    console.log("starting loading "+fileToRead)

    $.get(fileToRead, function(response) {

        //var options={"separator":","}
        var lines = $.csv.toArrays(response,{"separator":"\t"})
        //firstLine = lines.shift()
        //LStream[propertyName]=arrayToFloat(firstLine.slice(1,firstLine.length))
        for(var iL in lines) {
            line = lines[iL]
            edge = line[0]

            tempArray = line.slice(1,line.length)
            //console.log("---------------"+edge)
            allEdges[edge][propertyName]=[]
            for (el in tempArray){
                splited = tempArray[el].split(":")
                ident=splited[0]
                val = parseFloat(splited[1])
                allEdges[edge][propertyName][ident]=val

            }
        }

        asyncronousFunctionEnded(propertyName);
    },"text").fail(function() {
        console.log("file not found: "+fileToRead)

        LStream[propertyName]=[]
        for (edge in allEdges){
            allEdges[edge][propertyName]=[]
        }
        asyncronousFunctionEnded(propertyName);
        //console.log("oups")
        //alert("woops");
    });

}
*/

function loadNodeExplicitStat(fileToRead,propertyName){
    console.log("starting loading "+fileToRead)

    $.get(fileToRead, function(response) {

        //var options={"separator":","}
        var lines = $.csv.toArrays(response,{"separator":"\t"})
        //firstLine = lines.shift()
        //LStream[propertyName]=arrayToFloat(firstLine.slice(1,firstLine.length))
        for(var iL in lines) {
            line = lines[iL]
            node = line[0]

            tempArray = line.slice(1,line.length)
            //console.log("---------------"+node)
            allNodes[node][propertyName]=[]
            for (el in tempArray){
                splited = tempArray[el].split(":")
                ident=splited[0]
                val = splited[1]
                allNodes[node][propertyName][ident]=val

            }
        }

        asyncronousFunctionEnded(propertyName);
    },"text").fail(function() {
        console.log("file not found: "+fileToRead)

        LStream[propertyName]=[]
        for (node in allNodes){
            allNodes[node][propertyName]=[]
        }
        asyncronousFunctionEnded(propertyName);
        //console.log("oups")
        //alert("woops");
    });

}

function loadLSproperties(fileToRead) {
    console.log("starting loading " + fileToRead)

    $.get(fileToRead, function (response) {

        //var options={"separator":","}
        var lines = $.csv.toArrays(response, {"separator": "\t"})
        firstLine = lines.shift()
        LStream["properties"] = []
        for (var iL in lines) {
            line = lines[iL]
            property = line[0]
            value = line[1]
            LStream["properties"][property] = value
        }

        asyncronousFunctionEnded(fileToRead);
    }, "text").fail(function () {
        console.log("file not found: " + fileToRead)
    });
}

function loadNodeOrder(fileToRead) {
    console.log("starting loading " + fileToRead)

    $.get(fileToRead, function (response) {

        //var options={"separator":","}
        var lines = $.csv.toArrays(response, {"separator": "\t"})
        //firstLine = lines.shift()
        //LStream["properties"] = []
        nodeOrder=[]
        for (var iL in lines) {
            nodeOrder.push(lines[iL][0])
        }
        console.log("node order: ")
        console.log(nodeOrder)
        asyncronousFunctionEnded(fileToRead);
    }, "text").fail(function () {
        console.log("file not found: " + fileToRead)
        asyncronousFunctionEnded(fileToRead);
    });
}