
package com.twitter.home_mixer.product.for_you.selector

import com.twitter.product_mixer.component_library.model.candidate.TweetCandidate
import com.twitter.product_mixer.core.functional_component.selector.Selector
import com.twitter.product_mixer.core.model.common.presentation.CandidateWithDetails
import com.twitter.product_mixer.core.pipeline.PipelineQuery
import com.twitter.home_mixer.product.for_you.feature_hydrator.ClickbaitTweetFeature

class ClickbaitTweetDemotionSelector extends Selector[PipelineQuery] {
  override def apply(
    query: PipelineQuery,
    candidates: Seq[CandidateWithDetails],
    remainingResults: Seq[CandidateWithDetails]
  ): Seq[CandidateWithDetails] = {
    candidates.sortBy { candidate =>
      val isClickbait = candidate.features.getOrElse(ClickbaitTweetFeature, false)
      if (isClickbait) 1 else 0
    }
  }
}
