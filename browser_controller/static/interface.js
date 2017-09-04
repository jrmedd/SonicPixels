var seqWidth = 500;
var seqHeight= 500;
var colorGroups = ['white','blue','red','yellow', 'green'];
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

$('#sequencer td').on('click', function(){
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
    'step': 0,
    'value': 120
});

$("#current-bpm").html(setBPM.value);

setBPM.on('change', function(bpm) {
  var currentBPM = parseInt(bpm);
  $("#current-bpm").html(parseInt(bpm));
  socket.emit('transport_message', {'data':{'parameter':'bpm','state':currentBPM}});
})
