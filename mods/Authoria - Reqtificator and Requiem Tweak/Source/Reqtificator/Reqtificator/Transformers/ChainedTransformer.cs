using Mutagen.Bethesda.Plugins.Records;

namespace Reqtificator.Transformers
{
    internal class ChainedTransformer<T, TI, TGetter> : Transformer<T, TI, TGetter> where T : MajorRecord, TI where TI : class, IMajorRecord, TGetter where TGetter : class, IMajorRecordGetter
    {
        private readonly Transformer<T, TI, TGetter> _thisTransform;
        private readonly Transformer<T, TI, TGetter> _nextTransform;

        public ChainedTransformer(Transformer<T, TI, TGetter> thisTransform, Transformer<T, TI, TGetter> nextTransform)
        {
            _thisTransform = thisTransform;
            _nextTransform = nextTransform;
        }

        public override TransformationResult<T, TGetter> Process(TransformationResult<T, TGetter> input)
        {
            var result = _thisTransform.Process(input);
            return result.IsSkipped() ? result : _nextTransform.Process(result);
        }
    }
}
