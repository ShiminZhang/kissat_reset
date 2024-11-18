#include "Thompson.hpp"

extern "C" int select_lever_C(double reset_wins, double reset_loses,
                          double noreset_wins, double noreset_loses,
                          double explore_wins, double explore_loses)
{
  return (select_lever(reset_wins, reset_loses,
                          noreset_wins, noreset_loses,
                          explore_wins, explore_loses));
}

template<class T>
size_t argmax(const std::vector<T>& v){
  return std::distance(v.begin(), std::max_element(v.begin(), v.end()));
}

unsigned int select_lever(double reset_wins, double reset_loses,
                          double noreset_wins, double noreset_loses,
                          double explore_wins, double explore_loses) {
    base_generator gen;

    std::vector<double> trials = {reset_loses, noreset_loses, explore_loses};
    std::vector<double> wins = {reset_wins, noreset_wins, explore_wins};

    std::vector<boost::random::beta_distribution<>> prior_dists = {
        boost::random::beta_distribution<>(reset_wins, reset_loses),
        boost::random::beta_distribution<>(noreset_wins, noreset_loses),
        boost::random::beta_distribution<>(explore_wins, explore_loses)};

    std::vector<double> priors;
    for (auto &dist : prior_dists) {
        priors.push_back(dist(gen));
    }

    return static_cast<unsigned int>(argmax(priors));
}
