if ($(window).width() > $(window).height()) {
  var seqWidth = $(window).height()*0.85;
  var seqHeight= $(window).height()*0.85;
}
else {
  var seqWidth = $(window).width()*0.85;
  var seqHeight= $(window).width()*0.85;
}
var colorGroups = ['white','#498AF4','#DD5044','#FECE44', '#17A460'];
var numVoices = 5;
var numSteps = 5;

for (var row = 0; row < numVoices; row ++) {
  var tr = $('<tr>');
  for (var col = 0; col < numSteps; col ++) {
    $('<td id="'+col+'-'+row+'-0" class="sequencer-cell white"></td>').appendTo(tr);
  }
  tr.appendTo('#sequencer');
};

$('#sequencer').css('width', seqWidth);
$('#sequencer').css('height', seqHeight);
$('#sequencer').css('margin', '0 auto');

/*
var timingSequencer = new Nexus.Sequencer("#timing-grid", {
  'size': [seqWidth, seqHeight/10],
  'rows':1,
  'columns':numSteps
});

var currentStep = 0;

timingSequencer.on('step', function(s) {
  currentStep = (currentStep+1)%numSteps;
});
*/
for (var i = 0; i < 5; i ++) {
  $('<div id="grid-'+i+'"></div>"').appendTo("#sequencing-grids");
}

var matrices = new Array();

for (var i = 0; i < 5; i++) {
  matrices.push(new Nexus.Sequencer("#grid-"+i, {'columns':numVoices, 'rows':numSteps }))
  matrices[i].on('change', function(c){
    var currentGrid = this.parent.id.split('-')[1];
    if (currentGrid != "0")
    socket.emit('grid_message', {'grid':currentGrid, 'data':c})
  });
  matrices[i].on('step', function(s) {
    //console.log(this.parent.id + " column " + currentStep + ": "+ s.reverse().join(', '));
  });
};

$('#sequencer td').on('click touch', function(){
  var cellValues = $(this).attr('id').split('-').map(Number);
  var matrixIndex = cellValues[2];
  $(this).removeClass(colorGroups[matrixIndex]);
  matrices[matrixIndex].matrix.set.cell(cellValues[0],cellValues[1], 0);
  matrixIndex = (matrixIndex + 1) % 5;
  matrices[matrixIndex].matrix.set.cell(cellValues[0],cellValues[1], 1);
  $(this).addClass(colorGroups[matrixIndex]);
  $(this).css('background', colorGroups[matrixIndex]);
  cellValues[2] = matrixIndex;
  $(this).attr('id',cellValues.join('-'));
});

var playbackToggle = new Nexus.TextButton('#toggle-playback',{
    'size': [150,50],
    'text': 'Play',
    'mode': 'toggle',
    'alternateText': 'Stop'
});

playbackToggle.alternateText = 'Stop';

playbackToggle.on('change', function(play) {
  socket.emit('transport_message', {'data':{'parameter':'playing','state':play}});
  /*
  if (play) {
    for (var i = 0; i < matrices.length; i ++) {
      matrices[i].start();
    }
    timingSequencer.start();
  }
  else {
    for (var i = 0; i < matrices.length; i ++) {
      matrices[i].stop();
    }
    timingSequencer.stop();
  }
  */
});

var setBPM = new Nexus.Slider('#set-bpm', {
    'size': [120,20],
    'mode': 'absolute',  // 'relative' or 'absolute'
    'min': 60,
    'max': 200,
    'step': 1,
    'value': 120
});


var bpmDisplay = new Nexus.Number('#current-bpm');
bpmDisplay.link(setBPM);

setBPM.on('change', function(bpm) {
  socket.emit('transport_message', {'data':{'parameter':'bpm','state':bpm}});
})
