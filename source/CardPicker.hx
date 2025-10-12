package;

import flixel.FlxSubState;

class CardPicker extends FlxSubState
{
    override public function create()
	{
		add(newCard(100, 200, "fireball", "testSubject1", 1.5));
	}
    
    function newCard(x:Float, y:Float, id:String, nickname:String, ?scale:Float = 1):Card
	{
		var card:Card = new Card(x, y, id, nickname, scale);
		return card;
	}

    override public function update(elapsed:Float)
	{
		super.update(elapsed);

        if (flixel.FlxG.keys.justPressed.ESCAPE)
        {
            close();
        }
	}
}