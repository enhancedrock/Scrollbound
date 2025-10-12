package;

import flixel.FlxG;
import flixel.FlxSprite;
import flixel.group.FlxGroup;
import flixel.text.FlxText;
import flixel.util.FlxColor;
import flixel.util.FlxSignal;
import haxe.Json;
import openfl.Assets;

typedef CardData = {
    var name:String;
    var description:String;
    var tp:Int;
}

class Card extends FlxSprite
{
    public var cardId:String;
    public var nickName:String;
    public var originalScale:Float;
    public var isHovered:Bool = false;

    private var originalY:Float;
    private var originalX:Float;
    
    // Integrated tooltip components
    private var tooltipGroup:FlxGroup;
    private var tooltipBackground:FlxSprite;
    private var titleText:FlxText;
    private var descriptionText:FlxText;
    private var tpText:FlxText;
    private var tooltipVisible:Bool = false;

    // signal that all cards can broadcast to
    public static var cardClickedSignal:FlxTypedSignal<String->Void> = new FlxTypedSignal<String->Void>();
    public static var cardCommandSignal:FlxTypedSignal<String->Void> = new FlxTypedSignal<String->Void>();

    public function new(x:Float, y:Float, id:String, nickName:String, ?scale:Float = 1)
    {
        super(x, y);
        this.cardId = id;
        this.originalY = y;
        this.originalX = x;
        this.nickName = nickName;
        this.originalScale = scale;

        loadGraphic("assets/images/" + id + ".png");
        this.scale.set(scale, scale);
        updateHitbox();

        // Initialize tooltip components
        createTooltip();

        cardCommandSignal.add(onCardCommand);
    }

    private function createTooltip():Void
    {
        tooltipGroup = new FlxGroup();
        
        tooltipBackground = new FlxSprite();
        tooltipBackground.makeGraphic(250, 120, FlxColor.fromRGB(40, 40, 40, 95));
        tooltipGroup.add(tooltipBackground);

        var textWidth:Float = tooltipBackground.width - 20;

        titleText = new FlxText(0, 0, textWidth, "");
        titleText.setFormat(null, 16, FlxColor.WHITE, "center");
        titleText.wordWrap = true;
        tooltipGroup.add(titleText);

        descriptionText = new FlxText(0, 30, textWidth, "");
        descriptionText.setFormat(null, 12, FlxColor.GRAY, "center");
        descriptionText.wordWrap = true;
        tooltipGroup.add(descriptionText);

        tpText = new FlxText(0, 90, textWidth, "");
        tpText.setFormat(null, 14, FlxColor.YELLOW, "center");
        tpText.italic = true;
        tooltipGroup.add(tpText);

        hideTooltip();
        
        // Add tooltip to the same parent as the card
        if (FlxG.state != null)
        {
            FlxG.state.add(tooltipGroup);
        }
    }

    override function update(elapsed: Float):Void
    {
        var mouseOverCard = FlxG.mouse.overlaps(this);

        if (mouseOverCard && !isHovered)
        {
            onHoverEnter();
        }
        else if (!mouseOverCard && isHovered)
        {
            onHoverExit();
        }

        if (isHovered)
        {
            showTooltip();
        }

        if (mouseOverCard && FlxG.mouse.justPressed)
        {
            onClick();
        }

        super.update(elapsed);
    }

    private function showTooltip():Void
    {
        if (tooltipVisible) return;
        
        var cardData:CardData = loadCardData(cardId);
        if (cardData == null) return;

        titleText.text = cardData.name;
        descriptionText.text = cardData.description;
        tpText.text = cardData.tp + "TP";

        // center tooltip horizontally under the card
        var tooltipX:Float = x + (width - tooltipBackground.width) / 2;
        var tooltipY:Float = y + height + 10;

        // keep tooltip on screen
        if (tooltipX + tooltipBackground.width > FlxG.width)
        {
            tooltipX = x - tooltipBackground.width - 10;
        }
        if (tooltipY + tooltipBackground.height > FlxG.height)
        {
            tooltipY = FlxG.height - tooltipBackground.height;
        }

        setTooltipPosition(tooltipX, tooltipY);
        setTooltipVisible(true);
    }

    private function hideTooltip():Void
    {
        setTooltipVisible(false);
    }

    private function setTooltipPosition(x:Float, y:Float):Void
    {
        tooltipBackground.setPosition(x, y);
        titleText.setPosition(x + 10, y + 10);
        descriptionText.setPosition(x + 10, y + 30);
        tpText.setPosition(x + 10, y + 90);
    }

    private function setTooltipVisible(visible:Bool):Void
    {
        tooltipVisible = visible;
        tooltipBackground.visible = visible;
        titleText.visible = visible;
        descriptionText.visible = visible;
        tpText.visible = visible;
    }

    private function loadCardData(cardId:String):CardData
    {
        var path = "assets/data/cards/" + cardId + ".json";
        if (!Assets.exists(path)) return null;

        var jsonString = Assets.getText(path);
        return Json.parse(jsonString);
    }

    private function onHoverEnter():Void
    {
        isHovered = true;
        y = originalY - (this.height * 0.05);
        x = originalX - (this.width * 0.05);

        this.scale.set(this.originalScale * 1.1, this.originalScale * 1.1);
        updateHitbox();
    }

    private function onHoverExit():Void
    {
        isHovered = false;
        y = originalY;
        x = originalX;

        this.scale.set(this.originalScale, this.originalScale);
        updateHitbox();
        
        hideTooltip();
    }

    private function onClick():Void
    {
        cardClickedSignal.dispatch(nickName);
        trace('Card ${nickName} clicked!');
    }

    private function onCardCommand(targetNickname:String):Void
    {
        if (targetNickname == nickName)
        {
            trace('Card ${nickName} received a command!');
            alpha = 0.5;
        }
    }
    
    override function destroy():Void
    {
        cardCommandSignal.remove(onCardCommand);
        if (tooltipGroup != null)
        {
            tooltipGroup.destroy();
        }
        super.destroy();
    }
}