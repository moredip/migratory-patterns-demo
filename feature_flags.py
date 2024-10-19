from flagsmith import Flagsmith
from openfeature import api
from openfeature_flagsmith.provider import FlagsmithProvider
from openfeature.contrib.hook.opentelemetry import TracingHook


def init_feature_flags():
    flagsmith = Flagsmith(
        environment_key="2H2HYbmhRXmnvgZc4uDLbK", api_url="http://localhost:8000/api/v1"
    )

    flagsmith_provider = FlagsmithProvider(
        client=flagsmith,
        # By enabling the use_flagsmith_defaults setting, you can instruct the OpenFeature SDK to use
        # the default logic included in the Flagsmith client as per the docs here:
        # https://docs.flagsmith.com/clients/server-side#managing-default-flags. This will override the
        # default provided at evaluation time in the OpenFeature SDK in most cases (excluding those where
        # an unexpected exception happens in the Flagsmith client itself).
        # Required: False
        # Default: False
        use_flagsmith_defaults=False,
        # By default, when evaluating the boolean value of a feature in the OpenFeature SDK, the Flagsmith
        # OpenFeature Provider will use the 'Enabled' state of the feature as defined in Flagsmith. This
        # behaviour can be changed to use the 'value' field defined in the Flagsmith feature instead by
        # enabling the use_boolean_config_value setting.
        # Note: this relies on the value being defined as a Boolean in Flagsmith. If the value is not a
        # Boolean, an error will occur and the default value provided as part of the evaluation will be
        # returned instead.
        # Required: False
        # Default: False
        use_boolean_config_value=True,
        # By default, the Flagsmith OpenFeature Provider will raise an exception (triggering the
        # OpenFeature SDK to return the provided default value) if the flag is disabled. This behaviour
        # can be configured by enabling this flag so that the Flagsmith OpenFeature provider ignores
        # the enabled state of a flag when returning a value.
        # Required: False
        # Default: False
        return_value_for_disabled_flags=False,
    )

    api.set_provider(flagsmith_provider)
    api.add_hooks([TracingHook()])
