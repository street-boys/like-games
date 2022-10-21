//
// Created by deded on 8/3/22.
//

#ifndef LIKE_TEXAS_HOLDEM_HPP
#define LIKE_TEXAS_HOLDEM_HPP

#include "poker/evaluator/holdem/holdem_equity_calculation.hpp"
#include "poker/evaluator/holdem/holdem_evaluation.hpp"
#include "poker/evaluator/holdem/holdem_result.hpp"
#include "poker/game/holdem/game.hpp"

#include "data_structure.hpp"

#include <drogon/drogon.h>

#include <stdexcept>
#include <sstream>
#include <string>
#include <vector>
#include <iomanip>

namespace like {
    namespace {
        auto side_pot_winners(const poker::game::holdem::gamecards &__cards,
                              const std::vector <uint64_t> &__eligible_player_indices) -> std::vector <std::pair<poker::evaluator::holdem::holdem_result, uint64_t>> {
            std::vector <std::pair<poker::evaluator::holdem::holdem_result, uint64_t>> winners;
            std::for_each(__eligible_player_indices.cbegin(), __eligible_player_indices.cend(),
                          [&](const uint64_t pos) {
                              winners.emplace_back(poker::evaluator::holdem::evaluate_unsafe(
                                      poker::cardset(__cards.m_board).combine(__cards.m_hands[pos].as_cardset())), pos);
                          });
            std::sort(winners.begin(), winners.end(),
                      [&](const auto &lhs, const auto &rhs) { return lhs.first > rhs.first; });
            const auto first_non_winner =
                    std::find_if(winners.cbegin() + 1, winners.cend(),
                                 [&](const auto &e) { return e.first < winners[0].first; });
            const auto dist = std::distance(winners.cbegin(), first_non_winner);

            winners.resize(dist, std::make_pair(poker::evaluator::holdem::holdem_result(0, 0, 0, 0), 0));

            return winners;
        }

        auto wins_in_percentages(
                const poker::evaluator::holdem::equity_calculation_result_t &__results) -> std::vector <std::pair<uint64_t, std::string>> {
            std::vector <std::pair<uint64_t, std::string>> wins;
            for (size_t index = 0; auto const &result: __results.m_equities) {
                wins.push_back(std::make_pair(index++, (std::stringstream{} << std::fixed
                                                                            << std::setprecision(2)
                                                                            << result).str()));
            }
            return wins;
        }
    } // namespace

    namespace poker {
        namespace net {
            namespace http {
                namespace holdem {
                    auto holdem_evaluator_router(const drogon::HttpRequestPtr &request,
                                                 std::function<void(
                                                         const drogon::HttpResponsePtr &)> &&callback) -> void {
                        auto request_json = glz::read_json<data_structures::evaluator_request_schema>(request->body());
                        data_structures::evaluator_response_schema response_json;

                        for (auto const &result: side_pot_winners(game::holdem::gamecards(request_json.board,
                                                                                          request_json.hands),
                                                                  request_json.players_index)) {
                            response_json.detail.winners.push_back(std::move(data_structures::hand_schema{
                                    .id=result.second,
                                    .hand=result.first.str_long()
                            }));
                        }

                        auto response = drogon::HttpResponse::newHttpResponse();
                        response->setContentTypeCode(drogon::ContentType::CT_APPLICATION_JSON);
                        response->setBody(glz::write_json(response_json));

                        callback(response);
                    }

                    auto holdem_equity_router(const drogon::HttpRequestPtr &request,
                                              std::function<void(const drogon::HttpResponsePtr &)> &&callback) -> void {
                        auto request_json = glz::read_json<data_structures::equities_request_schema>(request->body());
                        data_structures::equities_response_schema response_json;

                        for (auto const &win: wins_in_percentages(poker::evaluator::holdem::calculate_equities(
                                request_json.hands,
                                request_json.board
                        ))) {
                            response_json.detail.winners.push_back(std::move(data_structures::equities_result_schema{
                                    .id=win.first,
                                    .wins=win.second
                            }));
                        }
                        auto response = drogon::HttpResponse::newHttpResponse();
                        response->setContentTypeCode(drogon::ContentType::CT_APPLICATION_JSON);
                        response->setBody(glz::write_json(response_json));

                        callback(response);
                    }
                } // namespace holdem
            } // namespace http
        } // namespace net
    } // namespace poker
} // namespace like

#endif //LIKE_TEXAS_HOLDEM_HPP
