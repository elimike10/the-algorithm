
package com.twitter.home_mixer.product.for_you.feature_hydrator

import com.twitter.product_mixer.core.feature.Feature
import com.twitter.product_mixer.core.feature.featuremap.FeatureMap
import com.twitter.product_mixer.core.feature.featuremap.FeatureMapBuilder
import com.twitter.product_mixer.core.functional_component.feature_hydrator.CandidateFeatureHydrator
import com.twitter.product_mixer.core.model.common.identifier.FeatureHydratorIdentifier
import com.twitter.product_mixer.core.pipeline.PipelineQuery
import com.twitter.stitch.Stitch
import com.twitter.home_mixer.model.HomeFeatures.TweetTextFeature

object ClickbaitTweetFeature extends Feature[TweetCandidate, Boolean]

class ClickbaitTweetFeatureHydrator extends CandidateFeatureHydrator[PipelineQuery, TweetCandidate] {
  override val identifier: FeatureHydratorIdentifier = FeatureHydratorIdentifier("ClickbaitTweet")

  override val features: Set[Feature[_, _]] = Set(ClickbaitTweetFeature)

  override def hydrate(query: PipelineQuery, candidate: TweetCandidate): Stitch[FeatureMap] = {
    val tweetText = candidate.features.getOrElse(TweetTextFeature, "")
    val isClickbait = tweetText.toLowerCase.contains("here are") && tweetText.contains("🧵")
    
    Stitch.value(FeatureMapBuilder().add(ClickbaitTweetFeature, isClickbait).build())
  }
}
