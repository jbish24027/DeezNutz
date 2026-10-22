using System;
using FluentAssertions;
using Mutagen.Bethesda.Plugins;
using Mutagen.Bethesda.Skyrim;
using Noggog;
using Reqtificator.Configuration;
using Reqtificator.StaticReferences;
using Reqtificator.Transformers;
using Reqtificator.Transformers.Actors;
using Xunit;

namespace ReqtificatorTest.Transformers.Actors
{
    public class ActorAlreadyReqtifiedSkipTest
    {
        [Fact]
        public void Should_skip_actors_that_have_the_already_reqtified_keyword()
        {
            var transformer = new ActorAlreadyReqtifiedSkip()
                .AndThen(new PlayerChanges(new PlayerConfig(10, 20, 30,
                    Array.Empty<IFormLinkGetter<ISpellGetter>>())));

            var input = new Npc(FormKey.Factory("000007:Skyrim.esm"), SkyrimRelease.SkyrimSE)
            {
                Configuration = new NpcConfiguration { HealthOffset = 0, MagickaOffset = 0, StaminaOffset = 0 },
                Keywords = new ExtendedList<IFormLinkGetter<IKeywordGetter>> { Keywords.AlreadyReqtified }
            };

            var result = transformer.Process(new UnChanged<Npc, INpcGetter>(input));

            result.Should().BeOfType<Skipped<Npc, INpcGetter>>();
            result.Record().Equals(input).Should().BeTrue();
        }

        [Fact]
        public void Should_continue_processing_actors_without_the_already_reqtified_keyword()
        {
            var transformer = new ActorAlreadyReqtifiedSkip()
                .AndThen(new PlayerChanges(new PlayerConfig(10, 20, 30,
                    Array.Empty<IFormLinkGetter<ISpellGetter>>())));

            var input = new Npc(FormKey.Factory("000007:Skyrim.esm"), SkyrimRelease.SkyrimSE)
            {
                Configuration = new NpcConfiguration { HealthOffset = 0, MagickaOffset = 0, StaminaOffset = 0 }
            };

            var result = transformer.Process(new UnChanged<Npc, INpcGetter>(input));

            result.Should().BeOfType<Modified<Npc, INpcGetter>>();
            result.Record().Configuration.HealthOffset.Should().Be(10);
            result.Record().Configuration.MagickaOffset.Should().Be(20);
            result.Record().Configuration.StaminaOffset.Should().Be(30);
        }
    }
}
