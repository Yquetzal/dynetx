/**
 * Created by remy on 16/09/16.
 */
function populateLeftList(){
    var resultSearch = "";
    $("#resultSearch").empty()
    resultSearch+="<tr><th>display:</th></td>";

    possibleNodeAttributes.forEach(function(el){
        if(currentlyDisplayedAttribute==el){
            resultSearch+='<tr class="info">';
        }
        else{
            resultSearch+="<tr>";
        }

        resultSearch+="<td><div onclick=\"changeDisplayedPropertyTo('";

        resultSearch+=el+"')\">"
        resultSearch+=el+"</div></tr></td>";



    });
    //jQuery("#resultSearch").html(resultSearch);
    $("#resultSearch").append(resultSearch)

}

function populateTabLinkFlowProp(){
    var resultSearch = "Properties : ";
    $("#LinkSpropContent").empty()
    for(k in LStream["properties"]) {
        resultSearch += "<br>"+k+": "+LStream["properties"][k];
    }
    console.log("resultSearch: ")
    console.log(resultSearch)
    $("#LinkSpropContent").append(resultSearch)

}
function changeDisplayedPropertyTo(newProperty){
    console.log("changing for :"+newProperty)
    currentlyDisplayedAttribute=newProperty
    populateLeftList()
    computeNodePropertiesPath(newProperty)
    drawNodeProperties(newProperty)
    if(detailedEges)
        drawEdgeProperties(advancedEdgesPropertiesNames[0])

}