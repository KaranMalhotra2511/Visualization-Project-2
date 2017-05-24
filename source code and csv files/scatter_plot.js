function test1(){
	console.log('test1')

}

function test2(){
	console.log('test2');

}


function plot_values_stratified(filename) {
    console.log("i am here");
    
    filename = "./data/" + filename;
    svg.selectAll("*").remove();
    
    // Load data
    d3.csv(filename, function(error, data) {
        console.log("data ",data);
        data.forEach(function(d) {
            d.a1 = +d.a1;
            d.a2 = +d.a2;
        });

        var xValueR = function(d) { return d.a1;};
        var yValueR = function(d) { return d.a2;};
        
        xScale.domain([d3.min(data, xValueR), d3.max(data, xValueR)]);
        yScale.domain([d3.min(data, yValueR), d3.max(data, yValueR)]);
        
        
        svg.append("g")
            .attr("class", "axis")
            .attr("transform", "translate(0, "+(h-pad-10)+")")
            .call(xAxis);

        svg.append("g")
            .attr("class", "axis")
            .attr("transform", "translate("+(left_pad-pad)+", 0)")
            .call(yAxis);

        svg.append("text")
            .attr("transform", "rotate(-90)")
            .attr("y", left_pad-80)
            .attr("x",h-600)
            .attr("dy", "1em")
            .style("text-anchor", "middle")
            .text("Component A");

        svg.append("text")
            .attr("y", h-20)
            .attr("x", h+250)
            .attr("dy", "1em")
            .style("text-anchor", "middle")
            .text("Component B");


        svg.selectAll("circle")
            .data(data)
            .enter()
            .append("circle")
            .attr("r", 2.5)
            .attr("cx", function(d){
                return xScale(d.a1);
            }) 
            .attr("cy", function(d){
                return yScale(d.a2);
            }) 
            .style("fill", "blue");

    });

}

function plot_values(filename) {
    
    filename = "./data/" + filename;
    svg.selectAll("*").remove();
    
    // Load data
    d3.csv(filename, function(error, data) {
        data.forEach(function(d) {
            d.r1 = +d.r1;
            d.r2 = +d.r2;
            
        });

        var xValueR = function(d) { return d.r1;};
        var yValueR = function(d) { return d.r2;};
        
        xScale.domain([d3.min(data, xValueR), d3.max(data, xValueR)]);
        yScale.domain([d3.min(data, yValueR), d3.max(data, yValueR)]);
        
        
        svg.append("g")
            .attr("class", "axis")
            .attr("transform", "translate(0, "+(h-pad-10)+")")
            .call(xAxis);

        svg.append("g")
            .attr("class", "axis")
            .attr("transform", "translate("+(left_pad-pad)+", 0)")
            .call(yAxis);

        svg.append("text")
            .attr("transform", "rotate(-90)")
            .attr("y", left_pad-80)
            .attr("x",h-600)
            .attr("dy", "1em")
            .style("text-anchor", "middle")
            .text("Component A");

        svg.append("text")
            .attr("y", h-20)
            .attr("x", h+250)
            .attr("dy", "1em")
            .style("text-anchor", "middle")
            .text("Component B");

        svg.selectAll("circle")
            .data(data)
            .enter()
            .append("circle")
            .attr("r", 2.5)
            .attr("cx", function(d){
                return xScale(d.r1);
            }) 
            .attr("cy", function(d){
                return yScale(d.r2);
            }) 
            .style("fill", "blue");
    });

}




