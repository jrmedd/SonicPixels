outlets = 1;

function hexlify_bits(input) {
	var theNumber = parseInt(input, 2);
	var theHex = theNumber.toString(16);
	while (theHex.length < 2) {
		theHex = "0" + theHex;
	}
	outlet(0, theHex);
}

function hexlify_integer(input) {
	var theHex = input.toString(16);
	while (theHex.length < 2) {
		theHex = "0" + theHex;
	}
	outlet(0, theHex);
}
