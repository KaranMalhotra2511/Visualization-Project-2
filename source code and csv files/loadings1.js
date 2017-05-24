function plot_loadings(filename) {
  filename = "./data/" + filename;
  svg.selectAll("*").remove();

  var margin = {top: 20, right: 20, bottom: 70, left: 40},
      width = 600 - margin.left - margin.right,
      height = 300 - margin.top - margin.bottom;

  var x = d3.scale.ordinal().rangeRoundBands([0, width], .05);

  var y = d3.scale.linear().range([height, 0+10]);

  var xAxis = d3.svg.axis()
                .scale(x)
                .orient("bottom");

  var yAxis = d3.svg.axis()
                .scale(y)
                .orient("left")
                .ticks(10);

  d3.csv(filename, function(error, data) {



      data.forEach(function(d,i) {
          d.date = +d.PCA_components;
          d.value = +d.eigen_value;
          
      });
      data.sort(function(x, y){
          return d3.descending(x.eigen_value, y.eigen_value);
      })
   
    x.domain(data.map(function(d) { return d.PCA_components; }));
    y.domain([0, d3.max(data, function(d) { return d.eigen_value; })]);

    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(100," + height + ")")
        .call(xAxis)
        .selectAll("text")
        .style("text-anchor", "end")
        .attr("dx", "-.8em")
        .attr("dy", "-.55em")
        .attr("transform", "rotate(-90)" );

    svg.append("text")
        .attr("transform", "translate(" + ((width/3)+50) + " ," + (height + margin.bottom) + ")")
        .style("text-anchor", "middle")
        .text(" ");

    svg.append("g")
        .attr("class", "y axis")
        .attr("transform", "translate(100,0)")
        .call(yAxis)
        .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end");

    svg.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", left_pad-70)
        .attr("x",h-500)
        .attr("dy", "1em")
        .style("text-anchor", "middle")
        .text(" ");

    var bar = svg.selectAll("bar")
        .data(data)
        .enter().append("rect")
        .attr("class", "rect")
        .style("fill", function(d,i){ if(i<3){return "green";} else {return "blue";}})//"steelblue")
        .attr("transform", "translate(100,0)")
        .attr("x", function(d,i) { return x(d.PCA_components)+(6*i); })
        .attr("width", x.rangeBand())
        .attr("y", function(d) { return y(d.eigen_value); })
        .attr("height", function(d) { return height - y(d.eigen_value); });


     
    bar.on("mouseenter", function(d,i) {

        d3.select(this)
            .transition()
            .duration(100)
            .attr("width", x.rangeBand()+5)
            .style("fill","red")
            .style("z-index",2)
            .style("filter", "none");
    });
      bar.on("mouseout", function(d,i) {
          console.log("i before ",i)
          d3.select(this)

              .transition()
              .duration(100)
              .style("fill", function(){
                  console.log("i ",i)
                  if(i<3){console.log("i nblblbl ",i) ;return "green";} else {return "blue";}})
              .attr("width", x.rangeBand())
              .style("z-index",0)
              .style("filter", "none");
      });
});
}