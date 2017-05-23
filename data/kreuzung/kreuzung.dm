# An einer Wegkreuzung
Du stehst auf einer Stelle, an der sich zwei Wege kreuzen. Der breitere
der beiden Wege läuft von Ost nach West. Ein schmalerer Weg verläuft
von Nordosten nach Südwesten.

Sonderbarerweise kannst du keinem der beiden Wege folgen. Irgendetwas
hält dich hier. Vielleicht bist du einfach schon zu lange auf den Beinen
gewesen, um jetzt noch eine lange Reise anzutreten.

Direkt nördlich der Kreuzung steht ein einzelnes Haus.

## Haus
Im Norden siehst du das einzige Haus weit und breit. Es sieht aus wie
eine Herberge. Das bietet sich ja auch an, hier, wo sich zwei wichtige
Verkehrswege kreuzen.
.alias
herberge, gasthaus, hütte


// Hauptstraße: der breite Weg:
## Weg
. {ich.ist(magier)}
Als Magier erkennst du natürlich sofort, dass der breite Weg durch einen
starken Zauber geschützt sind.
. {else}
Der breite Weg ist irgendwie unbegehbar, aber wieso nur?
..add {hier.ist(regen)}
So matschig wie die Straße durch den Regen geworden ist, willst
du dort sowieso nicht längsgehen.
.adjektive
breit
.alias Hauptstraße, Straße
### Schutzzauber {ich.ist(magier)}
Ein wirklich mächtiger Schutzzauber liegt auf dem Weg. Du findest keine
Anhaltspunkte, wo der Zauber herkommt, aber du wirst sicher nicht gegen
ihn gegenankommen. Du wirst wohl nicht so einfach von dieser
Kreuzung wegkommen.


// Die Wachstraße: der schmale Weg
## Weg
Der schmalere Weg ist ganz klar unbetretbar. Aber wieso bloß?

## Weg {ich.ist(magier)}
Der schmalere Weg ist eigentich gar nicht magisch geschützt, aber der
Schutzzauber auf dem Hauptweg ist so stark, dass er beide Wege blockiert.


# :exits
## norden: vorplatz
