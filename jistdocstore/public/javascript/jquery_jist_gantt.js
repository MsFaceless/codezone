/* 
 * Copyright JIST
 * Date: 29 March 2014
 * All rights reserved.
 */

// Constructor which initializes the canvas widget
function JistGanttView(element) {
    this.canvas = document.getElementById(element);
    this.context = this.canvas.getContext("2d");
    var docw = document.width;
    var open_space = 10;
    this.stepx;
    this.stepy;
    this.alignValues = ['start', 'center', 'end'],
    this.baselineValues = ['top', 'middle', 'bottom',
                      'alphabetic', 'ideographic', 'hanging'],
    //this.canvas.width = $(document).width() - open_space;
    this.canvas.width = $(this.canvas).parent().width() - open_space;
    this.canvas.height = $(this.canvas).parent().height() - open_space;
    this.context.font = '12pt Helvetica';
    //console.log($(this.canvas).parent().height());
}
JistGanttView.prototype.drawGrid = function(color,startx,starty,stepx,stepy)
{
   this.context.save()
   this.stepx = stepx;
   this.stepy = stepy;
   var colno = 0;
   var rowno = 0;

   this.context.strokeStyle = color;
   this.context.fillStyle = '#ffffff';
   this.context.lineWidth = 0.5;
   this.context.fillRect(0, 0, this.canvas.width, this.canvas.height);
   this.context.strokeRect(0, 0, this.canvas.width, this.canvas.height);

   for (var i = startx + 0.5; i < this.canvas.width; i += stepx) {
     colno += 1;
     this.context.beginPath();
     this.context.moveTo(i, starty);
     this.context.lineTo(i, this.canvas.height);
     this.context.stroke();
     //this.context.fillText(text, posy, posx,maxsize);
     this.context.fillStyle = 'black';
     //this.context.fillText(colno, i, 10, stepx);
   }

   for (var i = starty + 0.5; i < this.canvas.height; i += stepy) {
     rowno += 1;
     this.context.beginPath();
     this.context.moveTo(startx, i);
     this.context.lineTo(this.canvas.width, i);
     this.context.stroke();
     this.context.fillStyle = 'black';
     //this.context.fillText(rowno, 10, i,stepy);
   }

   this.context.restore();
};
JistGanttView.prototype.drawLabels = function(color,toplabel,yearlabel,monthlabel)
{
     this.context.save()

     this.context.restore();
};

JistGanttView.prototype.drawLabels = function() {
    this.context.fillStyle = 'yellow';
    this.context.fillRect  (x, y, 7, 7);
    this.context.strokeRect(x, y, 7, 7);
}

JistGanttView.prototype.drawText = function(text, posx, posy, maxsize, textAlign, textBaseline) {
    if(textAlign) this.context.textAlign = textAlign;
    if(textBaseline) this.context.textBaseline = textBaseline;
    //if(textLineWidth) this.context.lineWidth = textLineWidth;
    this.context.fillStyle = 'black';
    this.context.fillText(text, posy, posx,maxsize);
}

JistGanttView.prototype.drawRect = function(startx,starty,thiswidth,thisheight,rgba) {
    this.context.strokeStyle = 'black';
    this.context.beginPath();
    if (! rgba) {
        this.context.fillStyle = 'rgba(0,0,255,0.5)';
    }else{
        this.context.fillStyle = rgba
    };
    this.context.save();
    //this.context.lineJoin = 'round';
    this.context.shadowColor = "rgba(80,80,80,.3)";
    this.context.shadowBlur = "5";
    this.context.shadowOffsetX = "10";
    this.context.shadowOffsetY = "10";
    this.context.strokeRect(startx,starty,thiswidth,thisheight);
    this.context.fillRect(startx,starty,thiswidth,thisheight);
    this.context.stroke();
    this.context.restore();
}
JistGanttView.prototype.drawGanttBar = function(startx,starty,thiswidth,thisheight) {
    this.context.strokeStyle = 'red';
    this.context.beginPath();
    //var grad = this.context.createLinearGradient(startx, starty, startx+thiswidth, starty+thisheight);
    //grad.addColorStop(0, 'black');
    //grad.addColorStop(1, 'white');
    this.context.lineWidth = 0.3;
    this.context.fillStyle = 'rgba(0,250,0,0.5)';
    //this.context.fillStyle = grad;
    this.context.save();
    //console.log(startx, starty);
    //console.log(thiswidth, thisheight);
    //this.context.moveTo(20, 80);
    //this.context.lineTo(20 + 738, 80);
    this.context.lineJoin = 'round';
    this.context.shadowColor = "rgba(80,80,80,.3)";
    this.context.shadowBlur = "5";
    this.context.shadowOffsetX = "10";
    this.context.shadowOffsetY = "10";
    this.context.strokeRect(startx,starty,thiswidth,thisheight);
    this.context.fillRect(startx,starty,thiswidth,thisheight);
    this.context.stroke();
    this.context.restore();
}

$(document).ready(function() {
    //jist_gantt_view = new JistGanttView('jist_contract_gantt_canvas');
    //jist_gantt_view.drawGrid('black',20,20)
    //jist_gantt_view.drawRect()
    //jist_gantt_view.drawText('My First Contract This way',100,20,20,'start','bottom')
    //console.log('Got here');
});
