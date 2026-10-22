using Mutagen.Bethesda.Skyrim;
using Reqtificator.StaticReferences;
using Serilog;

namespace Reqtificator.Transformers.Weapons
{
    internal class WeaponFullExclusionSkip : Transformer<Weapon, IWeapon, IWeaponGetter>
    {
        public override TransformationResult<Weapon, IWeaponGetter> Process(
            TransformationResult<Weapon, IWeaponGetter> input)
        {
            if (input.Record().HasKeyword(Keywords.NoDamageRescaling) &&
                input.Record().HasKeyword(Keywords.NoWeaponReachRescaling) &&
                input.Record().HasKeyword(Keywords.NoWeaponSpeedRescaling))
            {
                Log.Debug("skipped weapon with full reqtificator exclusion keyword set");
                return new Skipped<Weapon, IWeaponGetter>(input.Record());
            }

            return input;
        }
    }
}
