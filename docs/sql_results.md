
1. Top run scorers
--------------------------------------------------
SELECT batter, SUM(batter_runs) as total_runs
            FROM fact_deliveries
            GROUP BY batter
            ORDER BY total_runs DESC
            LIMIT 5;

      batter  total_runs
0    V Kohli        9346
1  RG Sharma        7331
2   S Dhawan        6769
3  DA Warner        6567
4   KL Rahul        5828

2. Top wicket takers
--------------------------------------------------
SELECT bowler, SUM(is_wicket) as total_wickets
            FROM fact_deliveries
            WHERE is_wicket = 1 AND wicket_type NOT IN ('run out', 'retired hurt', 'obstructing the field')
            GROUP BY bowler
            ORDER BY total_wickets DESC
            LIMIT 5;

      bowler  total_wickets
0  YS Chahal            233
1    B Kumar            226
2  SP Narine            209
3  PP Chawla            192
4  JJ Bumrah            190

3. Orange Cap by season
--------------------------------------------------
WITH SeasonRuns AS (
                SELECT m.season, d.batter, SUM(d.batter_runs) as runs
                FROM fact_deliveries d
                JOIN fact_matches m ON d.match_id = m.match_id
                GROUP BY m.season, d.batter
            ),
            RankedScorers AS (
                SELECT season, batter, runs,
                       RANK() OVER(PARTITION BY season ORDER BY runs DESC) as rnk
                FROM SeasonRuns
            )
            SELECT season, batter, runs
            FROM RankedScorers
            WHERE rnk = 1
            ORDER BY season;

     season           batter  runs
0   2007/08         SE Marsh   616
1      2009        ML Hayden   572
2   2009/10     SR Tendulkar   618
3      2011         CH Gayle   608
4      2012         CH Gayle   733
5      2013       MEK Hussey   733
6      2014       RV Uthappa   660
7      2015        DA Warner   562
8      2016          V Kohli   973
9      2017        DA Warner   641
10     2018    KS Williamson   735
11     2019        DA Warner   692
12  2020/21         KL Rahul   676
13     2021       RD Gaikwad   635
14     2022       JC Buttler   863
15     2023     Shubman Gill   890
16     2024          V Kohli   741
17     2025  B Sai Sudharsan   759
18     2026    V Suryavanshi   776

4. Purple Cap by season
--------------------------------------------------
WITH SeasonWickets AS (
                SELECT m.season, d.bowler, SUM(d.is_wicket) as wickets
                FROM fact_deliveries d
                JOIN fact_matches m ON d.match_id = m.match_id
                WHERE d.is_wicket = 1 AND d.wicket_type NOT IN ('run out', 'retired hurt', 'obstructing the field')
                GROUP BY m.season, d.bowler
            ),
            RankedBowlers AS (
                SELECT season, bowler, wickets,
                       RANK() OVER(PARTITION BY season ORDER BY wickets DESC) as rnk
                FROM SeasonWickets
            )
            SELECT season, bowler, wickets
            FROM RankedBowlers
            WHERE rnk = 1
            ORDER BY season;

     season             bowler  wickets
0   2007/08      Sohail Tanvir       22
1      2009           RP Singh       23
2   2009/10            PP Ojha       21
3      2011         SL Malinga       28
4      2012           M Morkel       25
5      2013           DJ Bravo       32
6      2014          MM Sharma       23
7      2015           DJ Bravo       26
8      2016            B Kumar       23
9      2017            B Kumar       26
10     2018             AJ Tye       24
11     2019        Imran Tahir       26
12     2019           K Rabada       26
13  2020/21           K Rabada       32
14     2021           HV Patel       32
15     2022          YS Chahal       27
16     2023     Mohammed Shami       28
17     2024           HV Patel       24
18     2025  M Prasidh Krishna       25
19     2026           K Rabada       29

5. Team win percentage
--------------------------------------------------
WITH TeamMatches AS (
                SELECT team1 as team, match_id, winner FROM fact_matches WHERE team1 IS NOT NULL
                UNION ALL
                SELECT team2 as team, match_id, winner FROM fact_matches WHERE team2 IS NOT NULL
            )
            SELECT team, 
                   COUNT(match_id) as total_matches,
                   SUM(CASE WHEN team = winner THEN 1 ELSE 0 END) as total_wins,
                   ROUND(CAST(SUM(CASE WHEN team = winner THEN 1 ELSE 0 END) AS FLOAT) / COUNT(match_id) * 100, 2) as win_pct
            FROM TeamMatches
            GROUP BY team
            HAVING total_matches > 50
            ORDER BY win_pct DESC;

                           team  total_matches  total_wins  win_pct
0                Gujarat Titans             77          47    61.04
1           Chennai Super Kings            266         148    55.64
2                Mumbai Indians            291         155    53.26
3         Kolkata Knight Riders            278         140    50.36
4   Royal Challengers Bengaluru            286         143    50.00
5              Rajasthan Royals            251         123    49.00
6           Sunrisers Hyderabad            211         102    48.34
7          Lucknow Super Giants             72          34    47.22
8                  Punjab Kings            278         126    45.32
9                Delhi Capitals            281         125    44.48
10              Deccan Chargers             75          29    38.67

6. Team performance trends (Wins by Season)
--------------------------------------------------
WITH TeamSeasonWins AS (
                SELECT winner as team, season, COUNT(match_id) as wins
                FROM fact_matches
                WHERE winner IS NOT NULL AND winner != 'No Result'
                GROUP BY winner, season
            )
            SELECT team, season, wins,
                   LAG(wins) OVER(PARTITION BY team ORDER BY season) as prev_season_wins
            FROM TeamSeasonWins
            WHERE team IN ('Chennai Super Kings', 'Mumbai Indians')
            ORDER BY team, season;

                   team   season  wins  prev_season_wins
0   Chennai Super Kings  2007/08     9               NaN
1   Chennai Super Kings     2009     8               9.0
2   Chennai Super Kings  2009/10     9               8.0
3   Chennai Super Kings     2011    11               9.0
4   Chennai Super Kings     2012    10              11.0
5   Chennai Super Kings     2013    12              10.0
6   Chennai Super Kings     2014    10              12.0
7   Chennai Super Kings     2015    10              10.0
8   Chennai Super Kings     2018    11              10.0
9   Chennai Super Kings     2019    10              11.0
10  Chennai Super Kings  2020/21     6              10.0
11  Chennai Super Kings     2021    11               6.0
12  Chennai Super Kings     2022     4              11.0
13  Chennai Super Kings     2023    10               4.0
14  Chennai Super Kings     2024     7              10.0
15  Chennai Super Kings     2025     4               7.0
16  Chennai Super Kings     2026     6               4.0
17       Mumbai Indians  2007/08     7               NaN
18       Mumbai Indians     2009     5               7.0
19       Mumbai Indians  2009/10    11               5.0
20       Mumbai Indians     2011    10              11.0
21       Mumbai Indians     2012    10              10.0
22       Mumbai Indians     2013    13              10.0
23       Mumbai Indians     2014     7              13.0
24       Mumbai Indians     2015    10               7.0
25       Mumbai Indians     2016     7              10.0
26       Mumbai Indians     2017    11               7.0
27       Mumbai Indians     2018     6              11.0
28       Mumbai Indians     2019    10               6.0
29       Mumbai Indians  2020/21    11              10.0
30       Mumbai Indians     2021     7              11.0
31       Mumbai Indians     2022     4               7.0
32       Mumbai Indians     2023     9               4.0
33       Mumbai Indians     2024     4               9.0
34       Mumbai Indians     2025     9               4.0
35       Mumbai Indians     2026     4               9.0

7. Toss impact
--------------------------------------------------
SELECT 
                COUNT(*) as total_matches,
                SUM(CASE WHEN toss_winner = winner THEN 1 ELSE 0 END) as toss_and_match_winner,
                ROUND(CAST(SUM(CASE WHEN toss_winner = winner THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100, 2) as toss_win_impact_pct
            FROM fact_matches
            WHERE winner != 'No Result';

   total_matches  toss_and_match_winner  toss_win_impact_pct
0           1218                    628                51.56

8. Venue advantage (Home team advantage approximation by Toss Winner = Home)
--------------------------------------------------
SELECT venue,
                   COUNT(*) as matches_played,
                   SUM(CASE WHEN toss_winner = winner THEN 1 ELSE 0 END) as wins_by_toss_winner
            FROM fact_matches
            GROUP BY venue
            ORDER BY matches_played DESC
            LIMIT 5;

                              venue  matches_played  wins_by_toss_winner
0          Wankhede Stadium, Mumbai             132                   68
1             Eden Gardens, Kolkata             107                   53
2  M Chinnaswamy Stadium, Bengaluru             104                   55
3       Arun Jaitley Stadium, Delhi             104                   52
4   MA Chidambaram Stadium, Chennai              98                   49

9. Chasing success
--------------------------------------------------
SELECT 
                toss_decision,
                COUNT(*) as matches,
                SUM(CASE WHEN toss_winner = winner THEN 1 ELSE 0 END) as wins,
                ROUND(CAST(SUM(CASE WHEN toss_winner = winner THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100, 2) as win_pct
            FROM fact_matches
            WHERE toss_decision IN ('bat', 'field') AND winner != 'No Result'
            GROUP BY toss_decision;

  toss_decision  matches  wins  win_pct
0           bat      408   185    45.34
1         field      810   443    54.69

10. Powerplay performance (Overs 1-6)
--------------------------------------------------
SELECT batting_team,
                   SUM(total_runs) as powerplay_runs,
                   COUNT(DISTINCT match_id) as matches,
                   ROUND(CAST(SUM(total_runs) AS FLOAT) / COUNT(DISTINCT match_id), 2) as avg_powerplay_score
            FROM fact_deliveries
            WHERE over < 6
            GROUP BY batting_team
            ORDER BY avg_powerplay_score DESC
            LIMIT 5;

           batting_team  powerplay_runs  matches  avg_powerplay_score
0         Gujarat Lions            1559       30                51.97
1        Gujarat Titans            3998       77                51.92
2  Lucknow Super Giants            3729       72                51.79
3   Sunrisers Hyderabad           10695      210                50.93
4          Punjab Kings           13724      277                49.55

11. Death-over performance (Overs 16-20)
--------------------------------------------------
SELECT batting_team,
                   SUM(total_runs) as death_runs,
                   COUNT(DISTINCT match_id) as matches,
                   ROUND(CAST(SUM(total_runs) AS FLOAT) / COUNT(DISTINCT match_id), 2) as avg_death_score
            FROM fact_deliveries
            WHERE over >= 15
            GROUP BY batting_team
            ORDER BY avg_death_score DESC
            LIMIT 5;

                  batting_team  death_runs  matches  avg_death_score
0         Lucknow Super Giants        3448       71            48.56
1               Gujarat Titans        3660       76            48.16
2          Chennai Super Kings       12392      259            47.85
3  Royal Challengers Bengaluru       12652      266            47.56
4               Mumbai Indians       13238      279            47.45

12. Player consistency (30+ scores)
--------------------------------------------------
WITH BatterMatchScores AS (
                SELECT batter, match_id, SUM(batter_runs) as match_runs
                FROM fact_deliveries
                GROUP BY batter, match_id
            )
            SELECT batter,
                   COUNT(match_id) as innings_played,
                   SUM(CASE WHEN match_runs >= 30 THEN 1 ELSE 0 END) as scores_30_plus,
                   ROUND(CAST(SUM(CASE WHEN match_runs >= 30 THEN 1 ELSE 0 END) AS FLOAT) / COUNT(match_id) * 100, 2) as consistency_pct
            FROM BatterMatchScores
            GROUP BY batter
            HAVING innings_played > 50
            ORDER BY consistency_pct DESC
            LIMIT 5;

            batter  innings_played  scores_30_plus  consistency_pct
0  B Sai Sudharsan              57              38            66.67
1        H Klaasen              60              33            55.00
2         SE Marsh              69              37            53.62
3     Shubman Gill             130              68            52.31
4        DA Warner             184              96            52.17

13. Player-vs-team performance
--------------------------------------------------
SELECT batter, bowling_team, SUM(batter_runs) as total_runs
            FROM fact_deliveries
            WHERE batter = 'V Kohli'
            GROUP BY batter, bowling_team
            ORDER BY total_runs DESC
            LIMIT 5;

    batter           bowling_team  total_runs
0  V Kohli           Punjab Kings        1217
1  V Kohli    Chennai Super Kings        1174
2  V Kohli         Delhi Capitals        1172
3  V Kohli  Kolkata Knight Riders        1126
4  V Kohli         Mumbai Indians         977

14. Player-vs-venue performance
--------------------------------------------------
SELECT d.batter, m.venue, SUM(d.batter_runs) as runs
            FROM fact_deliveries d
            JOIN fact_matches m ON d.match_id = m.match_id
            WHERE d.batter = 'RG Sharma'
            GROUP BY d.batter, m.venue
            ORDER BY runs DESC
            LIMIT 5;

      batter                                          venue  runs
0  RG Sharma                       Wankhede Stadium, Mumbai  2632
1  RG Sharma                          Eden Gardens, Kolkata   500
2  RG Sharma                    Arun Jaitley Stadium, Delhi   489
3  RG Sharma  Rajiv Gandhi International Stadium, Hyderabad   429
4  RG Sharma                MA Chidambaram Stadium, Chennai   364

15. Winning margins (Average margin by runs)
--------------------------------------------------
SELECT winner,
                   AVG(win_margin_runs) as avg_win_margin_runs
            FROM fact_matches
            WHERE result_type = 'runs'
            GROUP BY winner
            ORDER BY avg_win_margin_runs DESC
            LIMIT 5;

Empty DataFrame
Columns: [winner, avg_win_margin_runs]
Index: []

16. Close matches (Won by <= 5 runs or <= 2 wickets)
--------------------------------------------------
SELECT winner, COUNT(*) as close_wins
            FROM fact_matches
            WHERE (result_type = 'runs' AND win_margin_runs <= 5)
               OR (result_type = 'wickets' AND win_margin_wickets <= 2)
            GROUP BY winner
            ORDER BY close_wins DESC
            LIMIT 5;

Empty DataFrame
Columns: [winner, close_wins]
Index: []

17. Early wicket impact (Lost wicket in 1st over)
--------------------------------------------------
WITH WicketFirstOver AS (
                SELECT DISTINCT match_id, batting_team
                FROM fact_deliveries
                WHERE over = 0 AND is_wicket = 1
            )
            SELECT COUNT(w.match_id) as matches_with_early_wicket,
                   SUM(CASE WHEN w.batting_team = m.winner THEN 1 ELSE 0 END) as wins_despite_early_wicket,
                   ROUND(CAST(SUM(CASE WHEN w.batting_team = m.winner THEN 1 ELSE 0 END) AS FLOAT) / COUNT(w.match_id) * 100, 2) as win_pct
            FROM WicketFirstOver w
            JOIN fact_matches m ON w.match_id = m.match_id;

   matches_with_early_wicket  wins_despite_early_wicket  win_pct
0                        480                        173    36.04

18. Target-range success (180+ targets)
--------------------------------------------------
WITH FirstInnings AS (
                SELECT match_id, SUM(total_runs) as target_score
                FROM fact_deliveries
                WHERE innings = 1
                GROUP BY match_id
            ),
            SecondInningsTeam AS (
                SELECT DISTINCT match_id, batting_team as chasing_team
                FROM fact_deliveries
                WHERE innings = 2
            )
            SELECT 
                COUNT(*) as total_180_chases,
                SUM(CASE WHEN s.chasing_team = m.winner THEN 1 ELSE 0 END) as successful_chases,
                ROUND(CAST(SUM(CASE WHEN s.chasing_team = m.winner THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100, 2) as success_pct
            FROM FirstInnings f
            JOIN SecondInningsTeam s ON f.match_id = s.match_id
            JOIN fact_matches m ON f.match_id = m.match_id
            WHERE f.target_score >= 180;

   total_180_chases  successful_chases  success_pct
0               443                140         31.6

19. Team recent form (Rolling 5 matches win pct)
--------------------------------------------------
WITH MatchResults AS (
                SELECT date, winner, team1, team2
                FROM fact_matches
                WHERE winner != 'No Result'
            ),
            TeamMatches AS (
                SELECT date, team1 as team, CASE WHEN winner = team1 THEN 1 ELSE 0 END as won FROM MatchResults
                UNION ALL
                SELECT date, team2 as team, CASE WHEN winner = team2 THEN 1 ELSE 0 END as won FROM MatchResults
            ),
            RollingForm AS (
                SELECT team, date, won,
                       AVG(won) OVER (PARTITION BY team ORDER BY date ROWS BETWEEN 4 PRECEDING AND CURRENT ROW) as rolling_win_pct
                FROM TeamMatches
            )
            SELECT team, date, ROUND(rolling_win_pct * 100, 2) as form_pct
            FROM RollingForm
            WHERE team = 'Chennai Super Kings'
            ORDER BY date DESC
            LIMIT 5;

                  team        date  form_pct
0  Chennai Super Kings  2026-05-21      40.0
1  Chennai Super Kings  2026-05-18      60.0
2  Chennai Super Kings  2026-05-15      60.0
3  Chennai Super Kings  2026-05-10      80.0
4  Chennai Super Kings  2026-05-05      60.0

20. Performance comparison (Batting Average vs Strike Rate)
--------------------------------------------------
WITH BatterStats AS (
                SELECT batter, 
                       SUM(batter_runs) as runs, 
                       COUNT(*) as balls,
                       SUM(is_wicket) as outs
                FROM fact_deliveries
                GROUP BY batter
                HAVING runs > 1000
            )
            SELECT batter, 
                   runs,
                   ROUND(CAST(runs AS FLOAT) / NULLIF(outs, 0), 2) as batting_average,
                   ROUND(CAST(runs AS FLOAT) / balls * 100, 2) as strike_rate
            FROM BatterStats
            ORDER BY strike_rate DESC
            LIMIT 5;

          batter  runs  batting_average  strike_rate
0  V Suryavanshi  1028            44.70       217.34
1        PD Salt  1258            33.11       168.63
2       TH David  1151            32.89       165.14
3     AD Russell  2655            28.86       163.28
4        TM Head  1556            32.42       162.25
