using FluentAssertions;
using Mutagen.Bethesda.Plugins;
using Mutagen.Bethesda.Skyrim;
using Noggog;
using Reqtificator.StaticReferences;
using Reqtificator.Transformers;
using Reqtificator.Transformers.Weapons;
using Xunit;

namespace ReqtificatorTest.Transformers.Weapons
{
    public class WeaponFullExclusionSkipTest
    {
        [Fact]
        public void Should_skip_weapons_that_have_the_full_exclusion_keyword_set()
        {
            var transformer = new WeaponFullExclusionSkip()
                .AndThen(new WeaponCriticalDamageScaling());

            var input = new Weapon(FormKey.Factory("123456:Requiem.esp"), SkyrimRelease.SkyrimSE)
            {
                Keywords = new ExtendedList<IFormLinkGetter<IKeywordGetter>>
                {
                    Keywords.NoDamageRescaling,
                    Keywords.NoWeaponReachRescaling,
                    Keywords.NoWeaponSpeedRescaling
                },
                BasicStats = new WeaponBasicStats { Damage = 99 },
                Critical = new CriticalData { Damage = 1 }
            };

            var result = transformer.Process(new UnChanged<Weapon, IWeaponGetter>(input));

            result.Should().BeOfType<Skipped<Weapon, IWeaponGetter>>();
            result.Record().Equals(input).Should().BeTrue();
        }

        [Fact]
        public void Should_continue_processing_weapons_without_the_full_exclusion_keyword_set()
        {
            var transformer = new WeaponFullExclusionSkip()
                .AndThen(new WeaponCriticalDamageScaling());

            var input = new Weapon(FormKey.Factory("123456:Requiem.esp"), SkyrimRelease.SkyrimSE)
            {
                Keywords = new ExtendedList<IFormLinkGetter<IKeywordGetter>>
                {
                    Keywords.NoDamageRescaling,
                    Keywords.NoWeaponReachRescaling
                },
                BasicStats = new WeaponBasicStats { Damage = 99 },
                Critical = new CriticalData { Damage = 1 }
            };

            var result = transformer.Process(new UnChanged<Weapon, IWeaponGetter>(input));

            result.Should().BeOfType<Modified<Weapon, IWeaponGetter>>();
            result.Record().Critical!.Damage.Should().Be(99);
        }
    }
}
