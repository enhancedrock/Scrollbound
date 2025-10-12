package;

import flixel.FlxG;
import flixel.FlxState;
import flixel.text.FlxText;
import flixel.ui.FlxButton;
import flixel.util.FlxColor;
import flixel.util.FlxGradient;
import flixel.util.FlxSave;

class MenuState extends FlxState
{
	function newGame()
    {
        var activerun:FlxSave = new FlxSave();
		activerun.bind("activerun");

		activerun.erase();
		newSave();
		
		FlxG.switchState(PlayState.new);
    }
	function continueGame()
    {		
		var activerun:FlxSave = new FlxSave();
		activerun.bind("activerun");

		if (activerun.data == null || activerun.data.floor == null) {
			newSave();
			return;
		}
		
		FlxG.switchState(PlayState.new);
    }

	function newSave()
	{
		var activerun:FlxSave = new FlxSave();
		activerun.bind("activerun");

		activerun.data.hp = 30;
		activerun.data.maxHp = 30;
		activerun.data.tp = 2;
		activerun.data.maxTp = 2;
		activerun.data.gold = 0;
		activerun.data.effects = [];
		activerun.data.floor = 0;
		activerun.data.biome = "none";
		activerun.data.deck = [];
		activerun.data.stockpile = [];

		activerun.flush();
	}

    override public function create()
	{
		var activerun:FlxSave = new FlxSave();
		activerun.bind("activerun");

		var buttonWidth = 480;
		var buttonHeight = 80;
		var gradientGraphic = FlxGradient.createGradientFlxSprite(
			buttonWidth, 
			buttonHeight, 
			[FlxColor.fromRGB(25, 25, 112), FlxColor.fromRGB(70, 130, 180)],
			1, 
			360
		);

		var newGameButton:FlxButton;
        newGameButton = new FlxButton(0, 0, "NEW RUN", newGame);
		newGameButton.loadGraphic(gradientGraphic.pixels);
		newGameButton.label.setFormat(null, 48, FlxColor.WHITE, "center");
		newGameButton.screenCenter();
		add(newGameButton);

		var continueGameButton:FlxButton;
		continueGameButton = new FlxButton(newGameButton.x, newGameButton.y - 20, "CONTINUE", continueGame);
		continueGameButton.loadGraphic(gradientGraphic.pixels);
		continueGameButton.label.setFormat(null, 48, FlxColor.WHITE, "center");
		continueGameButton.y = newGameButton.y + newGameButton.height + 30;
		add(continueGameButton);

		var titleText:FlxText;
		titleText = new FlxText(0, 0, FlxG.width, "SCROLLBOUND");
		titleText.setFormat(null, 96, FlxColor.WHITE, "center");
		titleText.y = newGameButton.y - titleText.height - 20;
		add(titleText);

		super.create();
	}

	override public function update(elapsed:Float)
	{
		super.update(elapsed);
	}
}
