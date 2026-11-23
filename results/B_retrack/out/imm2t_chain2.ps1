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
Write-Log 'coordinator 00:18: option (b) chosen; sa2 (option a) not run'
if ((Invoke-Step 'sa2rec') -ne 0) { Write-Log 'sa2rec FAILED; stop'; exit 1 }
if ((Invoke-Step 'kq') -ne 0) { Write-Log 'kq (record note) FAILED'; exit 1 }
Write-Log 'chain2 done'
