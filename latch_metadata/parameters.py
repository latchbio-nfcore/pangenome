
from dataclasses import dataclass
import typing
import typing_extensions

from flytekit.core.annotation import FlyteAnnotation

from latch.types.metadata import NextflowParameter
from latch.types.file import LatchFile
from latch.types.directory import LatchDir, LatchOutputDir

# Import these into your `__init__.py` file:
#
# from .parameters import generated_parameters

generated_parameters = {
    'input': NextflowParameter(
        type=LatchFile,
        default=None,
        section_title='Input/output options',
        description='Path to BGZIPPED input FASTA to build the pangenome graph from.',
    ),
    'n_haplotypes': NextflowParameter(
        type=float,
        default=None,
        section_title=None,
        description='The number of haplotypes in the input FASTA.',
    ),
    'outdir': NextflowParameter(
        type=typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})],
        default=None,
        section_title=None,
        description='The output directory where the results will be saved. You have to use absolute paths to storage on Cloud infrastructure.',
    ),
    'email': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Email address for completion summary.',
    ),
    'multiqc_title': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='MultiQC report title. Printed as page header, used for filename if not otherwise specified.',
    ),
    'wfmash_map_pct_id': NextflowParameter(
        type=typing.Optional[float],
        default=90,
        section_title='Wfmash Options',
        description='Percent identity in the wfmash mashmap step.',
    ),
    'wfmash_segment_length': NextflowParameter(
        type=typing.Optional[str],
        default='5000',
        section_title=None,
        description='Segment length for mapping.',
    ),
    'wfmash_block_length': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Minimum block length filter for mapping.',
    ),
    'wfmash_mash_kmer': NextflowParameter(
        type=typing.Optional[int],
        default=19,
        section_title=None,
        description='Kmer size for mashmap.',
    ),
    'wfmash_mash_kmer_thres': NextflowParameter(
        type=typing.Optional[float],
        default=0.001,
        section_title=None,
        description='Ignore the top % most-frequent kmers.',
    ),
    'wfmash_sparse_map': NextflowParameter(
        type=typing.Optional[str],
        default='1.0',
        section_title=None,
        description='Keep this fraction of mappings (`auto` for giant component heuristic).',
    ),
    'wfmash_merge_segments': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Merge successive mappings.',
    ),
    'wfmash_exclude_delim': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Skip mappings between sequences with the same name prefix before the given delimiter character. This can be helpful if several sequences originate from the same chromosome. It is recommended that the sequence names respect the https://github.com/pangenome/PanSN-spec. In future versions of the pipeline it will be required that the sequence names follow this specification.',
    ),
    'wfmash_chunks': NextflowParameter(
        type=typing.Optional[int],
        default=1,
        section_title=None,
        description='The number of files to generate from the approximate wfmash mappings to scale across a whole cluster. It is recommended to set this to the number of available nodes. If only one machine is available, leave it at 1.',
    ),
    'wfmash_only': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='If this parameter is set, only the wfmash alignment step of the pipeline is executed. This option is offered for users who want to run wfmash on a cluster.',
    ),
    'wfmash_hg_filter_ani_diff': NextflowParameter(
        type=typing.Optional[int],
        default=30,
        section_title=None,
        description='Filter out mappings unlikely to be this Average Nucleotide Identity (ANI) less than the best mapping.',
    ),
    'wfmash_n_mappings': NextflowParameter(
        type=typing.Optional[int],
        default=None,
        section_title=None,
        description='Number of mappings for each segment. [default: `n_haplotypes - 1`].',
    ),
    'seqwish_min_match_length': NextflowParameter(
        type=typing.Optional[int],
        default=23,
        section_title='Seqwish Options',
        description='Ignores exact matches below this length.',
    ),
    'seqwish_transclose_batch': NextflowParameter(
        type=typing.Optional[str],
        default='10000000',
        section_title=None,
        description='Number of base pairs to use for transitive closure batch.',
    ),
    'seqwish_sparse_factor': NextflowParameter(
        type=typing.Optional[float],
        default=0,
        section_title=None,
        description='Keep this randomly selected fraction of input matches.',
    ),
    'seqwish_paf': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Input PAF file. The wfmash alignment step is skipped.',
    ),
    'skip_smoothxg': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title='Smoothxg options',
        description='Skip the graph smoothing step of the pipeline.',
    ),
    'smoothxg_poa_length': NextflowParameter(
        type=typing.Optional[str],
        default='700,900,1100',
        section_title=None,
        description='Maximum sequence length to put int POA. Is a comma-separated list. For each integer, SMOOTHXG wil be executed once.',
    ),
    'smoothxg_pad_max_depth': NextflowParameter(
        type=typing.Optional[int],
        default=100,
        section_title=None,
        description="Path depth at which we don't pad the POA problem.",
    ),
    'smoothxg_poa_padding': NextflowParameter(
        type=typing.Optional[float],
        default=0.001,
        section_title=None,
        description="Pad each end of each seuqence in POA with 'smoothxg_poa_padding * longest_poa_seq' base pairs.",
    ),
    'smoothxg_poa_params': NextflowParameter(
        type=typing.Optional[str],
        default='1,19,39,3,81,1',
        section_title=None,
        description="Score parameters for POA in the form of 'match,mismatch,gap1,ext1,gap2,ext2'. It may also be given as presets: 'asm5', 'asm10', 'asm15', 'asm20'. [default: 1,19,39,3,81,1 = asm5].",
    ),
    'smoothxg_write_maf': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Write MAF output representing merged POA blocks.',
    ),
    'smoothxg_run_abpoa': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Run abPOA. [default: SPOA].',
    ),
    'smoothxg_run_global_poa': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Run the POA in global mode. [default: local mode].',
    ),
    'smoothxg_poa_cpus': NextflowParameter(
        type=typing.Optional[int],
        default=0,
        section_title=None,
        description="Number of CPUs for the potentially very memory expensive POA phase of SMOOTHXG. Default is 'task.cpus'.",
    ),
    'vcf_spec': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title='Vg Deconstruct Options',
        description='Specify a set of VCFs to produce with `--vcf_spec "REF[:LEN][,REF[:LEN]]*"`.',
    ),
    'communities': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title='Community',
        description='Enable community detection.',
    ),
    'multiqc_methods_description': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title='Generic options',
        description='Custom MultiQC yaml file containing HTML including a methods description.',
    ),
}

