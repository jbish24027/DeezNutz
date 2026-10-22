Scriptname ThalmorOnHitSetEnemyScript extends ReferenceAlias  

Event onHit(objectReference akAggressor, Form akWeapon, Projectile akProjectile, bool abPowerAttack, bool abSneakAttack, bool abBashAttack, bool abHitBlocked)
	if akAggressor == PlayerRef && enemyFaction && PlayerFaction
		enemyFaction.SetEnemy(PlayerFaction)
	endif
EndEvent

Event OnDying(Actor akKiller)
	Actor SoldierRef = Soldier.GetActorRef()
	if SoldierRef && SoldierRef.IsDead() == 0
		SoldierRef.EvaluatePackage()
	endif
EndEvent

Faction Property enemyFaction  Auto  

Faction Property PlayerFaction  Auto  

Actor Property PlayerRef  Auto  

ReferenceAlias Property Soldier  Auto  
