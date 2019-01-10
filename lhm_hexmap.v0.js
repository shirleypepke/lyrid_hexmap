// lyrid_hexmap v0.0.1 for online exploration of trained SOMs
// Copyright (c) 2019 Shirley Pepke (Lyrid, LLC) 
// This code is covered under an MIT license
/*
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */

// global vars
var width = 400;
var height = 400;
var data_queue = [];
var hexmaps = [];
var filelist = [];
var refsize = 200;
var numcols, numrows;
var hexRadius = 3;

// load dataset and create hexmap
function lhm_loadDataset(csvdat) {
    var dataset = d3.csvParse(csvdat);
    
    // validate that new map has same dimensions as those already placed. This is necessary for cross-referencing
    if (data_queue.length > 0) {
        var dncol = Math.max.apply(null, dataset.map(a => +a.ncol))+1;
        var dnrow = Math.max.apply(null, dataset.map(a => +a.nrow))+1;
        if ((dncol != numcols) || (dnrow != numrows)) {
            // throw error "Not loaded: Input map dimensions not same as currently loaded maps."
            alert("Loading of differently sized maps not allowed. Please select another file or clear the window and load again.");
            return;
        }
    }
    
   // set height and width according to hexRadius, ncol, and nrow
    if (data_queue.length === 0) {
        numcols = Math.max.apply(null, dataset.map(a => +a.ncol))+1;
        numrows = Math.max.apply(null, dataset.map(a => +a.nrow))+1;
        height = numrows * hexRadius * 1.5 + 20;
        width = numcols * hexRadius * 2 + 20;
    }
    
    
    data_queue.push(dataset);
    var hmap = lhm_genMap();
    hexmaps.push(hmap);
    // call reusable hexmap function for the data and set properties appropriately
    hmap.marginLeft((data_queue.length-1)*refsize).title(filelist[filelist.length-1].substring(0,filelist[filelist.length-1].length-4));
    if (data_queue.length > 1) { hmap.marginTop(-30); }
    d3.select("#chart").append("svg")
    .attr("width", width)
    .attr("height", height)
    .append("g")
    .attr("transform","translate(20,20)").datum(dataset).call(hmap);
    
}

// these defined events allow for dispatch of single hex events to corresponding hexagons in all hexmaps
d3.event = new MouseEvent('specialmouse');
d3.event.initMouseEvent('specialmouse');
d3.event = new MouseEvent('specialmouseout');
d3.event.initMouseEvent('specialmouseout');


function lhm_genMap() {
 
    var graphTitle;
    var marginLeft = 20, marginTop = 20;

    var points = []; // these will be the hexagon locations for this map

    // reusable hexmap 
    function lhm_hexmap(selection) {
        var dataset = selection.datum();
        var svg = selection;
        var hexselection=d3.select("nothing");
     
        for (var i =0; i<dataset.length; i++) {
            points.push([ hexRadius * (dataset[i].ncol * Math.sqrt(3.) + .5 * (dataset[i].nrow%2)), hexRadius * dataset[i].nrow * 1.5]);
        }
        
        var coordTip = d3.tip()
        .attr('class', 'd3-tip')
        .html(function(d) {
         // select hexagons across all maps
              hexselection = d3.selectAll(".hexagon").filter(function(dd,i) {return ((dd.nrow == d.nrow) && (dd.ncol == d.ncol))})
              hexselection.style("stroke","cyan").dispatch('specialmouse')          // color selected cell border highlight color in all maps and display coords
              return ""
        })
   
        // simulated tooltip in maps not under mouse location
        var specialTip = d3.tip()
        .attr('class', 'd3-tip')
        .html(function(d) { return "<span style='font-size:10px;color:cyan'> Row:"+d.nrow+", Col:"+d.ncol+", <br>Value:"+d.intensity+"</span>"})
        
        // attach tooltip event listeners to svg
        svg.call(coordTip);
        svg.call(specialTip);
 
        // use hexbin to create hexagonal containers
        var hexbin = d3.hexbin()
        .radius(hexRadius); //set the radius of each hexagon
        
        var hexbins = hexbin(points);
        for (let i = 0; i< hexbins.length; i++) {
            hexbins[i].intensity = dataset[i].intensity; // this value (in [0.,1.]) is what will be shown by unit color
            hexbins[i].nrow = dataset[i].nrow;
            hexbins[i].ncol = dataset[i].ncol;
            hexbins[i].highlight = 1; // attribute for unit highlight status
            hexbins[i].no = 'hex'+i; // unit index identifier for convenience
        }
        
        // customize colormaps for components vs. umatrix vs. bmu counts
        //this should be done at hexmap level, will swap ints for fracs for bmu counts
        function colormap(c) {
        if (graphTitle.includes("bmu")) {
            return d3.interpolateGreys(c); // problem is these values are integers - probably want to allow log scale too
        }
        if (graphTitle.includes("umx")) {
            return d3.interpolateBuPu(c);
        }
            return d3.interpolateRdYlBu(1.-c);
        }
        
        svg.append("div").attr("style","margin-left: "+marginLeft+"px; margin-top: " + marginTop+"px");
      
        // bind hexagon data to svg, position each hexagon, map unit colors, and add event handlers
        svg.append("g")
        .attr("class","geometry")
        .selectAll("path")
        .data(hexbins)
        .enter().append("path")
        .attr("class","hexagon")
        .attr("d", function(d) {
              // draw each hexagon moved to location d.x,d.y
              return "M" + d.x + "," + d.y + hexbin.hexagon();
              })
        .attr("fill",function(d) { return colormap(d.intensity); })
        .on('mouseover', coordTip.show)
        .on('mouseout', function(d) {
            hexselection.dispatch('specialmouseout'); // sync mouseout event across maps
           //coordTip.hide();
            })
        .on('specialmouse', specialTip.show)
        .on('specialmouseout', function(d) {
            if (d.highlight ==1) {
            if (!hexselection.empty()) {hexselection.style("stroke","none");}
              specialTip.hide(); } // remove highlight for unit on all maps
            else {
            
            // for each svg --> g --> data[index].intensity NOT d.intensity
            var index = +(d.no.substring(3,));
            // save clicked unit highlighting on all maps
            d3.selectAll("svg").select(".geometry").each(function(dd){d3.select(this).append("text").attr("class","typpy"+d.no).attr("fill","cyan").attr("text-anchor","start").attr("font-size","10px").attr("x",d.x).attr("y",d.y-20).text("Unit:"+d.nrow+","+d.ncol).append("tspan").attr("x", d.x).attr("dy",12).text("\nValue:"+(+dd[index].intensity).toFixed(2)); } )

            }
        })
        .on('click', function(d){
            d.highlight = d.highlight * -1.; // toggle highlight variable for unit
            if (d.highlight ==1) {
                var id = ".typpy"+d.no;
                d3.selectAll(id).remove(); // if highlighted unit has been clicked, remove tooltip text/highlight on all maps
            }
        })
        
        // turn off mouse events on text boxes
        svg.append("text").attr("pointer-events","none").style("font-size","16px").attr("y","-5px").text(graphTitle);

    }
    
    lhm_hexmap.marginLeft = hexmapMarginLeft;
    lhm_hexmap.marginTop = hexmapMarginTop;
    lhm_hexmap.title = hexmapTitle;
    lhm_hexmap.remove = hexmapRemove;
    
    // miscellaneous accessor functions
    function hexmapSVG() {
        return svg;
    }
    
    function hexmapMarginLeft(value) {
        marginLeft = value;
        return lhm_hexmap;
    }
    
    function hexmapMarginTop(value) {
        marginTop = value;
        return lhm_hexmap;
    }
    function hexmapTitle(value) {
        graphTitle = value;
        return lhm_hexmap;
    }
    
    function hexmapRemove(){
        d3.select("svg").remove();
    }
    
    return lhm_hexmap;
}

// handle upload button
function lhm_uploadButton(el, callback) {
    var uploader = document.getElementById(el);
    var reader = new FileReader();
    
    reader.onload = function(e) {
        var contents = e.target.result;
        d3.selectAll("#lotext").remove();
        callback(contents);
    };
    
    uploader.addEventListener("change", handleFiles, false);
    
    function handleFiles() {
        d3.select("#table").text("loading...").attr("id","lotext");
        var file = this.files[0];
        filelist.push(this.files[0].name);
        reader.readAsText(file);
    };
};

function lhm_clearButton() {
    hexmaps.forEach(function (elem) {
        elem.remove();
                    });
    data_queue.splice(0, data_queue.length);
    hexmaps.splice(0, hexmaps.length);
}
