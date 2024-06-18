import os
import shutil
import subprocess
import typing
from pathlib import Path

import requests
import typing_extensions
from flytekit.core.annotation import FlyteAnnotation
from latch.ldata.path import LPath
from latch.resources.tasks import custom_task, nextflow_runtime_task
from latch.resources.workflow import workflow
from latch.types import metadata
from latch.types.directory import LatchDir
from latch.types.file import LatchFile
from latch_cli.nextflow.utils import _get_execution_name
from latch_cli.nextflow.workflow import get_flag
from latch_cli.services.register.utils import import_module_by_path
from latch_cli.utils import urljoins

meta = Path("latch_metadata") / "__init__.py"
import_module_by_path(meta)


@custom_task(cpu=0.25, memory=0.5, storage_gib=1)
def initialize() -> str:
    token = os.environ.get("FLYTE_INTERNAL_EXECUTION_ID")
    if token is None:
        raise RuntimeError("failed to get execution token")

    headers = {"Authorization": f"Latch-Execution-Token {token}"}

    print("Provisioning shared storage volume... ", end="")
    resp = requests.post(
        "http://nf-dispatcher-service.flyte.svc.cluster.local/provision-storage",
        headers=headers,
        json={
            "storage_gib": 100,
        },
    )
    resp.raise_for_status()
    print("Done.")

    return resp.json()["name"]


@nextflow_runtime_task(cpu=4, memory=8, storage_gib=100)
def nextflow_runtime(
    pvc_name: str,
    input: LatchFile,
    n_haplotypes: float,
    outdir: typing_extensions.Annotated[LatchDir, FlyteAnnotation({"output": True})],
    email: typing.Optional[str],
    multiqc_title: typing.Optional[str],
    wfmash_block_length: typing.Optional[str],
    wfmash_merge_segments: typing.Optional[bool],
    wfmash_exclude_delim: typing.Optional[str],
    wfmash_only: typing.Optional[bool],
    wfmash_n_mappings: typing.Optional[int],
    seqwish_paf: typing.Optional[str],
    skip_smoothxg: typing.Optional[bool],
    smoothxg_write_maf: typing.Optional[bool],
    smoothxg_run_abpoa: typing.Optional[bool],
    smoothxg_run_global_poa: typing.Optional[bool],
    vcf_spec: typing.Optional[str],
    communities: typing.Optional[bool],
    multiqc_methods_description: typing.Optional[str],
    wfmash_map_pct_id: typing.Optional[float],
    wfmash_segment_length: typing.Optional[str],
    wfmash_mash_kmer: typing.Optional[int],
    wfmash_mash_kmer_thres: typing.Optional[float],
    wfmash_sparse_map: typing.Optional[str],
    wfmash_chunks: typing.Optional[int],
    wfmash_hg_filter_ani_diff: typing.Optional[int],
    seqwish_min_match_length: typing.Optional[int],
    seqwish_transclose_batch: typing.Optional[str],
    seqwish_sparse_factor: typing.Optional[float],
    smoothxg_poa_length: typing.Optional[str],
    smoothxg_pad_max_depth: typing.Optional[int],
    smoothxg_poa_padding: typing.Optional[float],
    smoothxg_poa_params: typing.Optional[str],
    smoothxg_poa_cpus: typing.Optional[int],
) -> None:
    try:
        shared_dir = Path("/nf-workdir")

        ignore_list = [
            "latch",
            ".latch",
            "nextflow",
            ".nextflow",
            "work",
            "results",
            "miniconda",
            "anaconda3",
            "mambaforge",
        ]

        shutil.copytree(
            Path("/root"),
            shared_dir,
            ignore=lambda src, names: ignore_list,
            ignore_dangling_symlinks=True,
            dirs_exist_ok=True,
        )

        cmd = [
            "/root/nextflow",
            "run",
            str(shared_dir / "main.nf"),
            "-work-dir",
            str(shared_dir),
            "-profile",
            "docker",
            "-c",
            "latch.config",
            *get_flag("input", input),
            *get_flag("n_haplotypes", n_haplotypes),
            *get_flag("outdir", outdir),
            *get_flag("email", email),
            *get_flag("multiqc_title", multiqc_title),
            *get_flag("wfmash_map_pct_id", wfmash_map_pct_id),
            *get_flag("wfmash_segment_length", wfmash_segment_length),
            *get_flag("wfmash_block_length", wfmash_block_length),
            *get_flag("wfmash_mash_kmer", wfmash_mash_kmer),
            *get_flag("wfmash_mash_kmer_thres", wfmash_mash_kmer_thres),
            *get_flag("wfmash_sparse_map", wfmash_sparse_map),
            *get_flag("wfmash_merge_segments", wfmash_merge_segments),
            *get_flag("wfmash_exclude_delim", wfmash_exclude_delim),
            *get_flag("wfmash_chunks", wfmash_chunks),
            *get_flag("wfmash_only", wfmash_only),
            *get_flag("wfmash_hg_filter_ani_diff", wfmash_hg_filter_ani_diff),
            *get_flag("wfmash_n_mappings", wfmash_n_mappings),
            *get_flag("seqwish_min_match_length", seqwish_min_match_length),
            *get_flag("seqwish_transclose_batch", seqwish_transclose_batch),
            *get_flag("seqwish_sparse_factor", seqwish_sparse_factor),
            *get_flag("seqwish_paf", seqwish_paf),
            *get_flag("skip_smoothxg", skip_smoothxg),
            *get_flag("smoothxg_poa_length", smoothxg_poa_length),
            *get_flag("smoothxg_pad_max_depth", smoothxg_pad_max_depth),
            *get_flag("smoothxg_poa_padding", smoothxg_poa_padding),
            *get_flag("smoothxg_poa_params", smoothxg_poa_params),
            *get_flag("smoothxg_write_maf", smoothxg_write_maf),
            *get_flag("smoothxg_run_abpoa", smoothxg_run_abpoa),
            *get_flag("smoothxg_run_global_poa", smoothxg_run_global_poa),
            *get_flag("smoothxg_poa_cpus", smoothxg_poa_cpus),
            *get_flag("vcf_spec", vcf_spec),
            *get_flag("communities", communities),
            *get_flag("multiqc_methods_description", multiqc_methods_description),
        ]

        print("Launching Nextflow Runtime")
        print(" ".join(cmd))
        print(flush=True)

        env = {
            **os.environ,
            "NXF_HOME": "/root/.nextflow",
            "NXF_OPTS": "-Xms2048M -Xmx8G -XX:ActiveProcessorCount=4",
            "K8S_STORAGE_CLAIM_NAME": pvc_name,
            "NXF_DISABLE_CHECK_LATEST": "true",
        }
        subprocess.run(
            cmd,
            env=env,
            check=True,
            cwd=str(shared_dir),
        )
    finally:
        print()

        nextflow_log = shared_dir / ".nextflow.log"
        if nextflow_log.exists():
            name = _get_execution_name()
            if name is None:
                print("Skipping logs upload, failed to get execution name")
            else:
                remote = LPath(urljoins("latch:///your_log_dir/nf_nf_core_pangenome", name, "nextflow.log"))
                print(f"Uploading .nextflow.log to {remote.path}")
                remote.upload_from(nextflow_log)


@workflow(metadata._nextflow_metadata)
def nf_nf_core_pangenome(
    input: LatchFile,
    n_haplotypes: float,
    outdir: typing_extensions.Annotated[LatchDir, FlyteAnnotation({"output": True})],
    email: typing.Optional[str],
    multiqc_title: typing.Optional[str],
    wfmash_block_length: typing.Optional[str],
    wfmash_merge_segments: typing.Optional[bool],
    wfmash_exclude_delim: typing.Optional[str],
    wfmash_only: typing.Optional[bool],
    wfmash_n_mappings: typing.Optional[int],
    seqwish_paf: typing.Optional[str],
    skip_smoothxg: typing.Optional[bool],
    smoothxg_write_maf: typing.Optional[bool],
    smoothxg_run_abpoa: typing.Optional[bool],
    smoothxg_run_global_poa: typing.Optional[bool],
    vcf_spec: typing.Optional[str],
    communities: typing.Optional[bool],
    multiqc_methods_description: typing.Optional[str],
    wfmash_map_pct_id: typing.Optional[float] = 90.0,
    wfmash_segment_length: typing.Optional[str] = "5000",
    wfmash_mash_kmer: typing.Optional[int] = 19,
    wfmash_mash_kmer_thres: typing.Optional[float] = 0.001,
    wfmash_sparse_map: typing.Optional[str] = "1.0",
    wfmash_chunks: typing.Optional[int] = 1,
    wfmash_hg_filter_ani_diff: typing.Optional[int] = 30,
    seqwish_min_match_length: typing.Optional[int] = 23,
    seqwish_transclose_batch: typing.Optional[str] = "10000000",
    seqwish_sparse_factor: typing.Optional[float] = 0.0,
    smoothxg_poa_length: typing.Optional[str] = "700,900,1100",
    smoothxg_pad_max_depth: typing.Optional[int] = 100,
    smoothxg_poa_padding: typing.Optional[float] = 0.001,
    smoothxg_poa_params: typing.Optional[str] = "1,19,39,3,81,1",
    smoothxg_poa_cpus: typing.Optional[int] = 0,
) -> None:
    """
    nf-core/pangenome

    Sample Description
    """

    pvc_name: str = initialize()
    nextflow_runtime(
        pvc_name=pvc_name,
        input=input,
        n_haplotypes=n_haplotypes,
        outdir=outdir,
        email=email,
        multiqc_title=multiqc_title,
        wfmash_map_pct_id=wfmash_map_pct_id,
        wfmash_segment_length=wfmash_segment_length,
        wfmash_block_length=wfmash_block_length,
        wfmash_mash_kmer=wfmash_mash_kmer,
        wfmash_mash_kmer_thres=wfmash_mash_kmer_thres,
        wfmash_sparse_map=wfmash_sparse_map,
        wfmash_merge_segments=wfmash_merge_segments,
        wfmash_exclude_delim=wfmash_exclude_delim,
        wfmash_chunks=wfmash_chunks,
        wfmash_only=wfmash_only,
        wfmash_hg_filter_ani_diff=wfmash_hg_filter_ani_diff,
        wfmash_n_mappings=wfmash_n_mappings,
        seqwish_min_match_length=seqwish_min_match_length,
        seqwish_transclose_batch=seqwish_transclose_batch,
        seqwish_sparse_factor=seqwish_sparse_factor,
        seqwish_paf=seqwish_paf,
        skip_smoothxg=skip_smoothxg,
        smoothxg_poa_length=smoothxg_poa_length,
        smoothxg_pad_max_depth=smoothxg_pad_max_depth,
        smoothxg_poa_padding=smoothxg_poa_padding,
        smoothxg_poa_params=smoothxg_poa_params,
        smoothxg_write_maf=smoothxg_write_maf,
        smoothxg_run_abpoa=smoothxg_run_abpoa,
        smoothxg_run_global_poa=smoothxg_run_global_poa,
        smoothxg_poa_cpus=smoothxg_poa_cpus,
        vcf_spec=vcf_spec,
        communities=communities,
        multiqc_methods_description=multiqc_methods_description,
    )
