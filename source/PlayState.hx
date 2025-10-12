package;

import flixel.FlxG;
import flixel.FlxState;
import flixel.text.FlxText;
import flixel.util.FlxColor;
import flixel.util.FlxSave;

class PlayState extends FlxState
{
	override public function create()
	{
		var titleText:FlxText;
		titleText = new FlxText(0, 0, FlxG.width, "LOAD");
		titleText.setFormat(null, 48, FlxColor.WHITE, "center");
		titleText.screenCenter();
		add(titleText);

		var activerun:FlxSave = new FlxSave();
		activerun.bind("activerun");

		if (activerun.data.floor == 0)
		{
			openSubState(new CardPicker());	
		}

		// listen for card clicks
		Card.cardClickedSignal.add(onCardClicked);
	}

	function newCard(x:Float, y:Float, id:String, nickname:String, ?scale:Float = 1):Card
	{
		var card:Card = new Card(x, y, id, nickname, scale);
		return card;
	}

	private function onCardClicked(nickName:String):Void
	{
		trace('PlayState received card click: ' + nickName);

		if (nickName == "testSubject1")
		{
			Card.cardCommandSignal.dispatch("testSubject1");
		}
	}

	override public function update(elapsed:Float)
	{
		super.update(elapsed);
	}
}
