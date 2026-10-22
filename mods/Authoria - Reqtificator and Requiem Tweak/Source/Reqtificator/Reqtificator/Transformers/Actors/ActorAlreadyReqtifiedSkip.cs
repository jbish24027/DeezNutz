using Mutagen.Bethesda.Skyrim;
using Reqtificator.StaticReferences;
using Serilog;

namespace Reqtificator.Transformers.Actors
{
    internal class ActorAlreadyReqtifiedSkip : Transformer<Npc, INpc, INpcGetter>
    {
        public override TransformationResult<Npc, INpcGetter> Process(TransformationResult<Npc, INpcGetter> input)
        {
            if (input.Record().HasKeyword(Keywords.AlreadyReqtified))
            {
                Log.Debug("skipped already reqtified actor");
                return new Skipped<Npc, INpcGetter>(input.Record());
            }

            return input;
        }
    }
}
