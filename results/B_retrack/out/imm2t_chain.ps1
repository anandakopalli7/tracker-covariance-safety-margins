$ErrorActionPreference = 'Stop'
Set-Location 'ARS_TRIAL\revision_v13\work\B_retrack\code'
$L = '..\out\imm2t\chain.log'
function Write-Log($m) { Add-Content -Path $L -Value ("{0} {1}" -f $m, (Get-Date -Format 'HH:mm:ss')) -Encoding utf8 }
function Invoke-Step($name) {
    Write-Log "$name start"
    $p = Start-Process -FilePath 'python' -ArgumentList '-I','-B','-X','utf8','b_imm2_tune_v01.py',$name `
        -RedirectStandardOutput "..\out\imm2t\$name.out" -RedirectStandardError "..\out\imm2t\$name.err" -WindowStyle Hidden -PassThru
    $null = $p.Handle
    $p.PriorityClass = 'BelowNormal'
    $p.WaitForExit()
    Write-Log "$name exit $($p.ExitCode)"
    return $p.ExitCode
}
if (-not (Test-Path '..\out\imm2t\IMM2_TUNE_CHECK_v01.json')) { if ((Invoke-Step 'check') -ne 0) { Write-Log 'check FAILED; stop'; exit 1 } }
$ok = & python -I -c "import json,sys; d=json.load(open(r'..\out\imm2t\IMM2_TUNE_CHECK_v01.json')); print(d['identical_to_frozen_run_stat'])"
if ($ok -ne 'True') { Write-Log 'identity NOT identical; stop'; exit 3 }
if ((Invoke-Step 'kq') -ne 0) { Write-Log 'kq FAILED; stop'; exit 1 }
if ((Invoke-Step 'sa2') -ne 0) { Write-Log 'sa2 FAILED; stop'; exit 1 }
Write-Log 'chain done'
