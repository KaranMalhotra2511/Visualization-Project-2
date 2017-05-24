function scree_plot(filename) {
    
    filename = "./data/" + filename;
    svg.selectAll("*").remove();
    
    // Set the dimensions of the canvas / graph
    var margin = {top: 30, right: 20, bottom: 50, left: 50},
        width = 800 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;

    // Set the ranges
    var x = d3.scale.linear().range([0, width]);
    var y = d3.scale.linear().range([height, 0]);

    // Define the axes
    var xAxis = d3.svg.axis().scale(x)
        .orient("bottom").ticks(18);

    var yAxis = d3.svg.axis().scale(y)
        .orient("left").ticks(7);

    // Define the line
    var valueline = d3.svg.line()
        .y(function(d) { return y(d.eigen_value); })
        .x(function(d) { return x(d.PCA_components); });

    var valueline2 = d3.svg.line()
        .y(function(d) { return y(1); })
        .x(function(d) { return x(d.PCA_components); });

        
    // Get the data
    d3.csv(filename, function(error, data) {
        data.forEach(function(d) {
            d.eigen_value = +d.eigan_values;
            d.PCA_components = +d.PCA_components;
        });

        // Scale the range of the data
        y.domain([0,d3.max(data, function(d) { return d.eigen_value; })+1]);
        x.domain(d3.extent(data, function(d) { return d.PCA_components; }));

        // Add the valueline path.
        svg.append("path")
            .attr("class", "line")
            .attr("d", valueline(data))
            .attr("transform", "translate(40,0)");
            // .attr("data-legend",function(d) { return d.name});

        svg.selectAll("dot")
            .data(data)
            .enter().append("circle")
            .style("fill", function(d,i){ if(d.eigen_value > 1){return "blue";} else {return "green";}})
            .attr("transform", "translate(40,0)")
            .attr("r", 4)
            .attr("cx", function(d) { return x(d.PCA_components); })
            .attr("cy", function(d) { return y(d.eigen_value); });

        svg.append("path")
            .attr("class", "line")
            .attr("transform", "translate(40,0)")
            .attr("d", valueline2(data))
            .attr("style","stroke:red" ); 

        
        // Add the X Axis
        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(40,"+ height+ ")")
            .call(xAxis);

        // Add the Y Axis
        svg.append("g")
            .attr("class", "y axis")
            .attr("transform", "translate(40,0)")
            .call(yAxis);

        // Add the text label for the Y axis
        svg.append("text")
            .attr("transform", "rotate(-90)")
            .attr("y", left_pad-100)
            .attr("x",height-400)
            .attr("dy", "1em")
            .style("text-anchor", "middle")
            .text("Eigen Values");

        svg.append("text")
            .attr("transform", "translate(" + (width / 2) + " ," + (height + margin.bottom) + ")")
            .style("text-anchor", "middle")
            .text("PCA Components");
            
       });

}