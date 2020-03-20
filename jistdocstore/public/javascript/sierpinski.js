/* 
 * Copyright 2012-2013 by Steffen A. Jakob (http://www.jakob.at/)
 * All rights reserved.
 */

// Constructor which initializes the canvas widget
function Sierpinski(element) {
    this.canvas = document.getElementById(element);
    this.context = this.canvas.getContext("2d");
    this.maxDepth = 10;
}
// Draw a Sierpinski Triangle with the given recursion depth
Sierpinski.prototype.drawSierpinskiTriangle = function(depth,width,angle)
{
    this.w = width;
    this.h = Math.sqrt(3) / 2 * this.w;
    this.canvas.width = this.w +100 ;
    this.canvas.height = this.h +100 ;
    this.context.save();
    this.context.scale(0.2,0.2);
    //this.context.translate(10,10)
    this.context.translate((this.w)/2+100,(this.h)/2+100);
    this.context.rotate(Math.PI/180 * angle);

    // Initialize the coordinates of an equilateral triangle which
    //var x0 = 0, y0 = this.h ;
    //var x1 = this.w, y1 = this.h;
    //var x2 = this.w/2, y2 = 0;
    var centx = this.w/2, centy = this.h/2
    var x0 = -this.w/2, y0 = this.h/2 ;
    var x1 = this.w/2, y1 = this.h/2;
    var x2 = 0, y2 = -this.h/2;
    //console.log(x2);
    // Draw the initial triangle (black)
    this.context.fillStyle = "#000";
    this.context.beginPath();
    this.context.moveTo(x0, y0);
    this.context.lineTo(x1, y1);
    this.context.lineTo(x2, y2);
    this.context.lineTo(x0, y0);
    this.context.closePath();
    this.context.lineWidth = 4;
    this.context.stroke();
    
    //this.drawTriangle(x0, y0, x1, y1, x2, y2);
    //console.log(x0,y0,x1,y1,x2,y2);
    this.context.beginPath();
    this.context.arc(0,0+80,this.h/2+95,0,2*Math.PI,false);
    this.context.closePath();
    this.context.strokeStyle = "#f00";
    this.context.lineWidth = 10;
    //this.context.lineWidth = 10;
    this.context.stroke();
    this.context.fillStyle = "#000";
    if (depth > this.maxDepth) { // make sure that depth doesn't get too high
        depth = this.maxDepth;
    }
    this.removeCenterTriangle(x0, y0, x1, y1, x2, y2, depth);    
    //this.context.save();
    this.context.beginPath();
    this.context.rect(0,0,10,10);
    this.context.closePath();
    this.context.fillStyle = "#f00";
    this.context.shadowBlur = 20;
    this.context.shadowColor = "#000";
    this.context.shadowOffsetX = 5;
    this.context.shadowOffsetY = 5;
    this.context.fillRect(0,0,10,10);
    this.context.restore();
};
Sierpinski.prototype.drawSierpinskiTriangleLogo = function(depth,width,angle)
{
    var canvas_space = 25;
    var arc_space_top = 16;
    var arc_space_sides = 25;
    var arc_line_width = 9;

    this.w = width;
    this.h = Math.sqrt(3) / 2 * this.w;
    this.canvas.width = this.w ;
    this.canvas.height = this.h  ;
    this.context.save();
    this.context.scale(0.5,0.5);
    
    //this.context.translate(10,10)
    this.context.translate((this.w)/2 + canvas_space,(this.h)/2+ + canvas_space);
    this.context.rotate(Math.PI/180 * angle);

    // Initialize the coordinates of an equilateral triangle which
    //var x0 = 0, y0 = this.h ;
    //var x1 = this.w, y1 = this.h;
    //var x2 = this.w/2, y2 = 0;
    var centx = this.w/2, centy = this.h/2
    var x0 = -this.w/2, y0 = this.h/2 ;
    var x1 = this.w/2, y1 = this.h/2;
    var x2 = 0, y2 = -this.h/2;
    //console.log(x2);
    // Draw the initial triangle (black)
    this.context.fillStyle = "#000";
    this.context.beginPath();
    this.context.moveTo(x0, y0);
    this.context.lineTo(x1, y1);
    this.context.lineTo(x2, y2);
    this.context.lineTo(x0, y0);
    this.context.closePath();
    this.context.lineWidth = arc_line_width;
    this.context.stroke();
    
    //this.drawTriangle(x0, y0, x1, y1, x2, y2);
    //console.log(x0,y0,x1,y1,x2,y2);
    this.context.beginPath();
    this.context.arc(0,0+arc_space_top,this.h/2+arc_space_sides,0,2*Math.PI,false);
    //this.context.arc(0,0+80,this.h/2+95,0,2*Math.PI,false);
    this.context.closePath();
    this.context.strokeStyle = "#f00";
    this.context.lineWidth = 5;
    //this.context.lineWidth = 10;
    this.context.stroke();
    this.context.fillStyle = "#000";
    if (depth > this.maxDepth) { // make sure that depth doesn't get too high
        depth = this.maxDepth;
    }
    this.removeCenterTriangle(x0, y0, x1, y1, x2, y2, depth);    
    //this.context.save();
    //this.context.beginPath();
    //this.context.rect(0,0,10,10);
    //this.context.closePath();
    this.context.fillStyle = "#f00";
    this.context.shadowBlur = 20;
    this.context.shadowColor = "#000";
    this.context.shadowOffsetX = 5;
    this.context.shadowOffsetY = 5;
    //this.context.fillRect(0,0,10,10);
    this.context.restore();
};
Sierpinski.prototype.drawSierpinskiTriangleVariable = function(depth,width,angle,canvas_space,arc_space_top,arc_space_sides,arc_line_width,scale)
{
    //var canvas_space = 25;
    //var arc_space_top = 16;
    //var arc_space_sides = 25;
    //var arc_line_width = 3;
    this.w = width;
    this.h = Math.sqrt(3) / 2 * this.w;
    this.canvas.width = this.w - canvas_space;
    this.canvas.height = this.h  ;
    this.context.save();
    this.context.scale(scale,scale);
    //this.context.scale(0.5,0.5);
    //this.context.translate(10,10)
    this.context.translate((this.w)/2 + canvas_space,(this.h)/2+ + canvas_space);
    this.context.rotate(Math.PI/180 * angle);

    // Initialize the coordinates of an equilateral triangle which
    //var x0 = 0, y0 = this.h ;
    //var x1 = this.w, y1 = this.h;
    //var x2 = this.w/2, y2 = 0;
    var centx = this.w/2, centy = this.h/2
    var x0 = -this.w/2, y0 = this.h/2 ;
    var x1 = this.w/2, y1 = this.h/2;
    var x2 = 0, y2 = -this.h/2;
    //console.log(x2);
    // Draw the initial triangle (black)
    this.context.fillStyle = "#000";
    this.context.beginPath();
    this.context.moveTo(x0, y0);
    this.context.lineTo(x1, y1);
    this.context.lineTo(x2, y2);
    this.context.lineTo(x0, y0);
    this.context.closePath();
    this.context.lineWidth = arc_line_width;
    this.context.stroke();
    
    //this.drawTriangle(x0, y0, x1, y1, x2, y2);
    //console.log(x0,y0,x1,y1,x2,y2);
    this.context.beginPath();
    this.context.arc(0,0+arc_space_top,this.h/2+arc_space_sides,0,2*Math.PI,false);
    //this.context.arc(0,0+80,this.h/2+95,0,2*Math.PI,false);
    this.context.closePath();
    this.context.strokeStyle = "#f00";
    this.context.lineWidth = arc_line_width*2;
    this.context.stroke();
    this.context.fillStyle = "#000";
    var fontsize = String(arc_line_width * 11) + 'px'
    this.context.font      = fontsize + " Helvetica-Oblique";
    this.context.fillStyle = "#000000";
    this.context.fillText('JIST',-this.canvas.width/4,this.canvas.height - canvas_space)
    if (depth > this.maxDepth) { // make sure that depth doesn't get too high
        depth = this.maxDepth;
    }
    this.removeCenterTriangle(x0, y0, x1, y1, x2, y2, depth);    
    //this.context.save();
    //this.context.beginPath();
    //this.context.rect(0,0,10,10);
    //this.context.closePath();
    this.context.fillStyle = "#f00";
    this.context.shadowBlur = 20;
    this.context.shadowColor = "#000";
    this.context.shadowOffsetX = 5;
    this.context.shadowOffsetY = 5;
    //this.context.fillRect(0,0,10,10);
    this.context.restore();
};

// Draw a filled triangle which is defined by the points
// (x0,y0), (x1,y1), and (x2,y2)
Sierpinski.prototype.drawTriangle = function(x0, y0, x1, y1, x2, y2) {
    this.context.beginPath();
    this.context.moveTo(x0, y0);
    this.context.lineTo(x1, y1);
    this.context.lineTo(x2, y2);
    this.context.lineTo(x0, y0);
    this.context.fill();
    this.context.closePath();
};

// Removes the center triangle which is defined by connecting the midpoints
// of each side.
Sierpinski.prototype.removeCenterTriangle = function(x0, y0, x1, y1, x2, y2, depth) {
    if (depth > 0) {
        // Midpoint coordinates
        var x01 = (x0 + x1)/2, y01 = (y0 + y1)/2;
        var x02 = (x0 + x2)/2, y02 = (y0 + y2)/2;
        var x12 = (x1 + x2)/2, y12 = (y1 + y2)/2;
        // Remove the center triangle
        this.drawTriangle(x01, y01, x02, y02, x12, y12);
        if (depth > 1) {
            // Recursively remove center triangles for the
            // remaining filled triangles
            this.removeCenterTriangle(x0, y0, x01, y01, x02, y02, depth - 1);
            this.removeCenterTriangle(x01, y01, x1, y1, x12, y12, depth - 1);
            this.removeCenterTriangle(x02, y02, x12, y12, x2, y2, depth - 1);
        }
    }
};
Sierpinski.prototype.drawBkgd = function()
{
    var spacing = 20;
    var ctx = this.context;
    //console.log(ctx);
    ctx.lineWidth = 1;    
    ctx.fillStyle = '#CCC';
    ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);    
    ctx.strokeStyle = '#EEE';    
    for (var i=0; i < this.canvas.width/spacing; i++) {
        var x = i*spacing;
        ctx.beginPath();        
        ctx.moveTo(x, 0)
        ctx.lineTo(x, this.canvas.height); 
        ctx.stroke(); 
        ctx.closePath();               
    };
    for (var i=0; i < this.canvas.height/spacing; i++) {
        var y = i*spacing;
        ctx.beginPath();
        ctx.moveTo(0, y)
        ctx.lineTo(this.canvas.width, y); 
        ctx.stroke();
        ctx.closePath();
    }; 
};
function sierpinski_init(){
        var depth = $("#slider_depth").val();
        var rotate_angle = $("#slider_rotation").val();
        var width = 550;
        //sierpinski.drawBkgd();
        //sierpinski.drawSierpinskiTriangle(depth,width,rotate_angle);
        i = 0;
        setInterval(function(){draw(depth,width,i+=40);},100);
        //for (i=0; i<361; i++) {
            //wait(100);
        //   console.log(i);
        //}
    
};
function draw(depth,width,rotate_angle){
    sierpinski = new Sierpinski();
    //sierpinski.drawBkgd();
    sierpinski.drawSierpinskiTriangle(depth,width,rotate_angle)

};
$(document).ready(function(){
    //$( "#logo1_canvas" ).click(function(){
    //    console.log("Clicked");
    //    )};
    $( "#slider_depth" ).change(function(e){
        //console.log("It helped");
        var val = $(this).val();
        var width = 550;
        var rotate_angle = $("#slider_rotation").val();
        //console.log(rotate_angle);
        sierpinski = new Sierpinski();
        sierpinski.drawBkgd();
        sierpinski.drawSierpinskiTriangle(val,width,rotate_angle);
    });
    $( "#slider_rotation" ).change(function(e){
        var depth = $("#slider_depth").val();
        var rotate_angle = $(this).val();
        var width = 550;
        sierpinski = new Sierpinski();
        sierpinski.drawBkgd();
        sierpinski.drawSierpinskiTriangle(depth,width,rotate_angle);

    });
    $(".logo_png").click(function(){
        //console.log("Clicked Pressed");
        var thisid = $(this).attr('id')
        //console.log(thisid);
        downloadlogos(thisid);

        
    });
});
