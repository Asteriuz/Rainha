$AudioDevice_A = "{0.0.0.00000000}.{2b7c39e9-b3e7-4659-9bcf-d93699c9d34b}"
$AudioDevice_B = "{0.0.0.00000000}.{9a22ca88-f5cf-4051-a55b-588ba84595df}"

# Toggle default playback device
$DefaultPlayback = Get-AudioDevice -Playback
If ($DefaultPlayback.ID -eq $AudioDevice_A) {Set-AudioDevice -ID $AudioDevice_B | Out-Null}
Else {Set-AudioDevice -ID $AudioDevice_A | Out-Null}
