@echo off
REM ============================================================================
REM Pipeline Complet Twitter - Découverte Automatique Comptes Députés
REM ============================================================================

echo.
echo ========================================================================
echo PIPELINE TWITTER - DÉCOUVERTE COMPTES DÉPUTÉS
echo ========================================================================
echo.

cd /d "%~dp0.."

REM Phase 1: Extraction Députés
echo.
echo [1/4] PHASE 1 : EXTRACTION DÉPUTÉS UNIQUES
echo ========================================================================
python scripts/phase1_extract_deputes.py
if %errorlevel% neq 0 (
    echo ERREUR Phase 1 - Arrêt
    pause
    exit /b 1
)

REM Phase 2: Génération Candidats
echo.
echo [2/4] PHASE 2 : GÉNÉRATION CANDIDATS USERNAMES
echo ========================================================================
python scripts/phase2_generate_candidates.py
if %errorlevel% neq 0 (
    echo ERREUR Phase 2 - Arrêt
    pause
    exit /b 1
)

REM Phase 3: Validation
echo.
echo [3/4] PHASE 3 : VALIDATION COMPTES (1-2h)
echo ========================================================================
echo Cette phase peut prendre 1-2 heures.
echo Progrès sauvegardé tous les 10 comptes.
echo Logs: logs/validation_log.txt
echo.
pause
node scripts/phase3_validate_accounts.js
if %errorlevel% neq 0 (
    echo ERREUR Phase 3 - Arrêt
    pause
    exit /b 1
)

REM Phase 4: Scraping Complet
echo.
echo [4/4] PHASE 4 : SCRAPING COMPLET (2-3h)
echo ========================================================================
echo Cette phase scrappe 100 tweets par compte validé.
echo.
pause
node scripts/phase4_scrape_validated.js
if %errorlevel% neq 0 (
    echo ERREUR Phase 4 - Arrêt
    pause
    exit /b 1
)

REM Résumé
echo.
echo ========================================================================
echo ✅ PIPELINE TERMINÉ
echo ========================================================================
echo.
echo Fichiers générés:
echo   - data/interim/deputes_unique.json
echo   - data/interim/twitter_candidates.json
echo   - data/interim/validated_accounts.json
echo   - data/processed/twitter_deputes_final.jsonl
echo   - logs/validation_log.txt
echo.
pause
