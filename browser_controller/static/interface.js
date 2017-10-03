//set variables for width and height of overall sequencer

if ($(window).width() > $(window).height()) {
  var seqWidth = $(window).height()*0.75;
  var seqHeight= $(window).height()*0.75;
}
else {
  var seqWidth = $(window).width()*0.75;
  var seqHeight= $(window).width()*0.75;
}

//names of sound banks
var soundBanks = ['haunted house','dawn chorus/nocturnal chorus','chronic coughs','sounds of space','bleeps and blips','ambient drones','static & noise','frequency bands']
//number of different sounds, and their representative colours (icluding white!)
var soundColours = ['FFFFFF','498AF4','DD5044','FECE44', '17A460', '64D9EF', 'F92653', '61C82D','F4BF75', '825078'];

//number of voices per step
var numVoices = 5;
//number of steps
var numSteps = 5;


//create select object for sound banks

var soundBankSelector = new Nexus.Select('#sound-bank', {
  'size' : [seqWidth*0.5, 40],
  'options': soundBanks
});

soundBankSelector.on('change', function(b){
  socket.emit('control_message',{'data':{'parameter':'sound-bank','state':b.index}})
});

//create volume slider

var volumeSlider = new Nexus.Slider("#volume-slider",{
  'size':[seqWidth*0.8, '40'],
  'min': 0,
  'max': 1,
  'step': 0,
  'value': 1,
  'mode':'absolute'
});

var volumeDisplay = new Nexus.Number('#current-volume', {
  'size': [seqWidth*0.125, 40]
});

volumeDisplay.link(volumeSlider);
volumeSlider.colorize("accent", "#"+soundColours[0]);

volumeSlider.on('change', function(v){
  socket.emit('control_message',{'data':{'parameter':'current-volume', 'state':v}});
  for (var i = 0; i < soundColours.length; i ++) {
    $("#colour-select-"+i).css('opacity',v);
  }
});

// create colour pickers

var colourSelect = new Array();
var selectedColour = 0;

for (var i = 0; i < soundColours.length; i ++) {
  $('<div class="interface-element"><div id="colour-select-'+i+'"></div></div>').appendTo($("#colours"));//append empty elements to the levels element
  colourSelect.push(new Nexus.Button("#colour-select-"+i, {
    'size':['40', '40'],
    'mode':'impulse'
  }));
  colourSelect[i].colorize("fill", "#"+soundColours[i]);
  colourSelect[i].colorize("accent", "#FFFFFF");
  colourSelect[i].on('change', function(s) {
    socket.emit('control_message',{'data':{'parameter':this.parent.id,'state':(s ? 1:0)}});
    selectedColour = this.parent.id.split("-")[2];
    volumeSlider.colorize("accent", "#"+soundColours[selectedColour]);
  });
};

//create the indivudal parent elements for the sequencers for each sound

for (var row = 0; row < numVoices; row ++) {
  var tr = $('<tr>');
  for (var col = 0; col < numSteps; col ++) {
    $('<td id="'+col+'-'+row+'-0" class="sequencer-cell"></td>').appendTo(tr);
  }
  tr.appendTo('#sequencer');
};

//set the size of the visible sequencer

$('#sequencer').css('width', seqWidth);
$('#sequencer').css('height', seqHeight);
$('#sequencer').css('margin', '0 auto');

for (var i = 0; i < soundColours.length; i ++) {
  $('<div id="grid-'+i+'"></div>"').appendTo("#sequencing-grids");
}


//create the matrices/sequencer objects for each sound

var matrices = new Array();

for (var i = 0; i < soundColours.length; i++) {
  matrices.push(new Nexus.Sequencer("#grid-"+i, {'columns':numVoices, 'rows':numSteps }))
  matrices[i].on('change', function(c){
    var currentGrid = this.parent.id.split('-')[1];
    if (currentGrid > "0")
    socket.emit('grid_message', {'grid':currentGrid, 'data':c})
  });
  matrices[i].on('step', function(s) {
    //console.log(this.parent.id + " column " + currentStep + ": "+ s.reverse().join(', '));
  });
};

//bind touch events for the interaction with the main sequencer

$('#sequencer td').on('click touch', function(){
  var cellValues = $(this).attr('id').split('-').map(Number);
  var matrixIndex = cellValues[2];
  $(this).removeClass(soundColours[matrixIndex]);
  matrices[matrixIndex].matrix.set.cell(cellValues[0],cellValues[1], 0);
  //matrixIndex = (matrixIndex + 1) % soundColours.length;
  matrixIndex = selectedColour;
  matrices[matrixIndex].matrix.set.cell(cellValues[0],cellValues[1], 1);
  $(this).addClass(soundColours[matrixIndex]);
  $(this).css('background',"#"+soundColours[matrixIndex]);
  $(this).css('opacity', (matrixIndex > 0)?volumeSlider.value:1);
  cellValues[2] = matrixIndex;
  $(this).attr('id',cellValues.join('-'));
});

//create the playback object

var playbackToggle = new Nexus.TextButton('#toggle-playback',{
    'size': [seqWidth*0.25, 40],
    'text': 'Play',
    'mode': 'toggle',
    'alternateText': 'Stop'
});

playbackToggle.alternateText = 'Stop';

playbackToggle.on('change', function(play) {
  socket.emit('control_message', {'data':{'parameter':'playing','state':(play ? 1:0)}});
});

var setBPM = new Nexus.Slider('#set-bpm', {
    'size': [seqWidth*0.25,15],
    'mode': 'absolute',
    'min': 60,
    'max': 200,
    'step': 1,
    'value': 120
});

var bpmDisplay = new Nexus.Number('#current-bpm', {
  'size': [seqWidth*0.125, 40]
});
bpmDisplay.link(setBPM);

setBPM.on('change', function(bpm) {
  socket.emit('control_message', {'data':{'parameter':'bpm','state':bpm}});
});
